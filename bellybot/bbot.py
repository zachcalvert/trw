import json
import random
import requests

import giphy_client
from giphy_client.rest import ApiException
import spacy

from bellybot import Responder
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


USER_MAP = {
    '4689709': ["lish", "greg"],
    '30833338': ["ne", "rene"],
    '22026356': ["shane", "shanye"],
    '30837253': ["jerad", "j-rock"],
    '30803449': ["ze", "vino", "zamsies"],
    '30837254': ["cam", "clam", "clambino"],
    '30837259': ["walsh"],
    '4037223': ["trav"],
    '87582812': ['justin', 'j-shaw'],
    '30837255': ['bk'],
    '30837252': ['D', 'commish', 'squirma'],
}


class BellyBot(Responder):

    def __init__(self):
        super().__init__()

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

    def send_gif(self, searches):
        gif = gif_search(random.choice(searches))
        if gif:
            return self.send_message(gif)

    def get_week_from_message(self, message, lookup):
        try:
            week_number = int(message.split('week ')[1].split(' {}'.format(lookup))[0])
        except (IndexError, ValueError):
            week_number = None
        return week_number

    def respond(self, sender, user_id, message):
        message = message.lower()
        print('message is {}'.format(message))

        if random.choice([1,2]) == 1:
            try:
                sender = random.choice(USER_MAP[user_id])
            except KeyError:
                pass

        if message.startswith('bad bot'):
            return self.send_message(f"sorry {sender}! Ill try not to send messages like that in the future")
        elif message.startswith('good bot'):
            return self.send_gif(['thank you', 'thanks', 'success', 'you rule', 'yay', 'yessss'])
        elif 'herbert' in message:
            return self.send_gif(['goat', 'the greatest of all time'])

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

                return self.send_message(response, image)

            elif first_word == 'gif':
                _, search_terms = message.split('bbot gif ')
                return self.send_gif(search_terms)

        if 'lions' in message:
            search = Answerer(sender=sender, message=message).go_lions()
            success, image = image_search(search)
            response = 'GO LIONS!'

            return self.send_message(response, image)

        if 'bbot' in message:
            if 'thanks' in message or 'thank you' in message or 'thx' in message:
                self.send_gif(['you\'re welcome', 'anytime', 'fist bump'])
                return
            elif 'power rankings' in message:
                response = espn_wrapper.get_power_rankings()
            elif 'trophies' in message:
                response = espn_wrapper.get_trophies(self.get_week_from_message(message, 'trophies'))
            elif 'projections' in message:
                response = espn_wrapper.get_projected_scoreboard()
            elif 'scoreboard' in message:
                response = espn_wrapper.scoreboard()
            elif 'standings' in message:
                response = espn_wrapper.standings()
            elif 'matchups' in message:
                response = espn_wrapper.matchups(self.get_week_from_message(message, 'matchups'))
            elif 'waiver' in message or 'pickup' in message:
                response = espn_wrapper.pickup()
            elif Answerer.should_answer(message):
                return Answerer(sender=sender, message=message).answer()
            else:
                response = self.generate_bbot_response(sender, message)
            return self.send_message(response)

        print('no bbot in this message')
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
        return None

    index = random.choice(range(20))
    try:
        gif = api_response.data[index]
    except IndexError:
        return None
    url = gif.images.downsized_large.url
    return url

