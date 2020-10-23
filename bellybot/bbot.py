import json
import random
import requests

import giphy_client
from giphy_client.rest import ApiException
import spacy

from bellybot.answerer import Answerer
from bellybot.espn_wrapper import ESPNWrapper
from bellybot.vocab.responses import MEMBER_RESPONSES, PLAYER_RESPONSES
from bellybot.vocab.rostered_players import NFL_PLAYERS

ESPN_URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2020/segments/0/leagues/832593"
GIPHY_API_KEY = "qUzMZY2GSYY8y"
GIS_ID = "cc646ee172e69377d"
GOOGLE_SEARCH_API_KEY = "AIzaSyCknrR34a7r"
GROUPME_URL = "https://api.groupme.com/v3/bots/post"

espn_wrapper = ESPNWrapper()
giphy_api_instance = giphy_client.DefaultApi()
nlp = spacy.load("en_core_web_sm")


class BellyBot:

    def __init__(self):
        self.identifier = "0ea167539344c9b1e822186071"

    def send_message(self, message, image=None):
        body = {
            "bot_id": self.identifier,
            "text": message
        }
        if image:
            body['attachments'] = [{
                "type": "image",
                "url": image
            }]

        headers = {'Content-Type': 'Application/json'}
        response = requests.post(GROUPME_URL, data=json.dumps(body), headers=headers)

        if response.status_code < 200 or response.status_code > 299:
            print('ERROR posting to GroupMe: {}: {}'.format(response.status_code, response.content))

    def _get_player(self, message):
        for player in NFL_PLAYERS.keys():
            if player in message:
                return NFL_PLAYERS[player]['full_name']
        return None

    def generate_bbot_response(self, sender, message):
        player = self._get_player(message)
        if player:
            random.shuffle(PLAYER_RESPONSES)
            response = PLAYER_RESPONSES.pop()
            response = response.replace('NFL_PLAYER', player)
        else:
            random.shuffle(MEMBER_RESPONSES)
            response = MEMBER_RESPONSES.pop()

        if 'BBR_MEMBER' in response:
            response = response.replace('BBR_MEMBER', sender)

        return response

    def respond(self, sender, message):
        image = None
        response = None
        message = message.lower()

        if message.startswith('bad bot'):
            return self.send_message(f"sorry {sender}! Ill try not to send messages like that in the future")

        if message.startswith('bbot '):
            _, command = message.split('bbot ', 1)
            try:
                first_word, _ = command.split(" ", 1)
            except ValueError:
                first_word = command

            if first_word == 'image':
                _, search_terms = message.split('bbot image ')
                response = search_terms
                success, image = image_search(search_terms)

            elif first_word == 'gif':
                _, search_terms = message.split('bbot gif ')
                success, gif = gif_search(search_terms)
                if success:
                    response = gif

        if not response and 'lions' in message:
            search = Answerer(sender=sender, message=message).go_lions()
            success, image = image_search(search)
            response = 'GO LIONS!'

        if not response and 'power rankings' in message:
            response = espn_wrapper.get_power_rankings()

        if not response and 'trophies' in message:
            response = espn_wrapper.get_trophies()

        if not response and 'projections' in message:
            response = espn_wrapper.get_projected_scoreboard()

        if not response and 'close matchups' in message:
            response = espn_wrapper.get_close_scores()

        if not response and 'bbot' in message:
            if Answerer.should_answer(message):
                response = Answerer(sender=sender, message=message).answer()
            if not response:
                response = self.generate_bbot_response(sender, message)

        print('received {}, so I am sending a response of {}'.format(message, response))

        if response:
            self.send_message(response, image)

        return


def image_search(search_terms):
    search_terms = search_terms.replace(" ", "%20")
    url =  f'https://www.googleapis.com/customsearch/v1?q={search_terms}&num=10&cx={GIS_ID}&searchType=image&key={GOOGLE_SEARCH_API_KEY}CP4PQ-z2IUhHouIR_GaLXFQ'
    response = requests.get(url)

    if response.status_code == 200:
        content = json.loads(response.content)
        if 'items' in content:
            index = random.choice(range(len(content['items'])))
            image_url = content['items'][index]['link']
            return True, image_url

    return False, None


def gif_search(search_terms):
    try:
        api_response = giphy_api_instance.gifs_search_get(GIPHY_API_KEY + "k1nOk2cOsKF3naPtlZF", search_terms, limit=20)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
        return False, None

    index = random.choice(range(20))
    try:
        gif = api_response.data[index]
    except IndexError:
        return False, None
    url = gif.images.downsized_large.url
    return True, url

