import json
import os
import random
import requests

import giphy_client
from giphy_client.rest import ApiException
import redis
import spacy

from bellybot.answerer import Answerer
from bellybot.context.actions import ACTIONS
from bellybot.context.people import ALL_PEOPLE, MEMBERS, PLAYERS
from bellybot.context.places import PLACES
from bellybot.context.reactions import ANTICIPATION_PREFIXES, ANTICIPATIONS, REACTION_PREFIXES, REACTIONS, CURRENT_PREFIXES
from bellybot.context.times import TIMES
from bellybot.responses import RESPONSES
from bellybot.vocab.rostered_players import NFL_PLAYERS

ESPN_URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2020/segments/0/leagues/832593"
GIPHY_API_KEY = "qUzMZY2GSYY8y"
GIS_ID = "cc646ee172e69377d"
GOOGLE_SEARCH_API_KEY = "AIzaSyCknrR34a7r"
GROUPME_URL = "https://api.groupme.com/v3/bots/post"

giphy_api_instance = giphy_client.DefaultApi()
nlp = spacy.load("en_core_web_sm")

redis_host = os.environ.get('REDISHOST', 'localhost')
cache = redis.StrictRedis(host=redis_host, port=6379)

class BellyBot:

    def __init__(self):
        self.identifier = "5cfd3e22f775c8db35033e9dd4"

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
        random.shuffle(RESPONSES)

        player = self._get_player(message)
        if player:
            response = next(r for r in RESPONSES if 'NFL_PLAYER' in r)
            m = RESPONSES.pop(RESPONSES.index(response))
            m = m.replace('NFL_PLAYER', player)
        else:
            response = next(r for r in RESPONSES if 'NFL_PLAYER' not in r)
            m = RESPONSES.pop(RESPONSES.index(response))

        if 'BBR_MEMBER' in m:
            m = m.replace('BBR_MEMBER', sender)

        print('length is now {}'.format(len(RESPONSES)))

        return m

    def respond(self, sender, message):
        image = None
        response = None
        message = message.lower()

        if message == 'bad bot':
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

        if 'lions' in message:
            search = Answerer(sender=sender, message=message).go_lions()
            success, image = image_search(search)
            response = 'GO LIONS!'

        if not response and 'bbot' in message:
            if Answerer.should_answer(message):
                response = Answerer(sender=sender, message=message).answer()
            if not response:
                response = self.generate_bbot_response(sender, message)

        print('received {}, so I am sending a response of {}'.format(message, response))

        if response:
            self.send_message(response, image)

        return

    def _increment_time(self, when):
        times = list(TIMES.keys())
        new_time = times[times.index(when) + 1]
        return new_time

    def create_context(self):
        subject = random.choice(ALL_PEOPLE)
        action = random.choice(list(ACTIONS.keys()))
        object = random.choice(ACTIONS[action]['objects'])
        location = random.choice(PLACES)

        bbot_context = {
            "who": ["bbot", subject],
            "where": location,
            "what": {
                "subject": subject,
                "action": action,
                "object":  object,
                "anticipation": random.choice(ANTICIPATIONS),
                "reaction":  random.choice(REACTIONS),
            },
            "when": "future",
        }

        if random.choice([1,2]) == 1:
            bbot_context["who"].append(random.choice(ALL_PEOPLE))

        cache.set("bbot", json.dumps(bbot_context))
        return bbot_context

    def get_context(self):
        try:
            context = json.loads(cache.get("bbot"))
            context['when'] = self._increment_time(context['when'])
        except (KeyError, IndexError):
            context = self.create_context()

        subject = context['what']['subject']
        when_helper = random.choice(TIMES[context['when']])
        action = ACTIONS[context['what']['action']][context['when']]
        object = context['what']['object']

        update = f'{subject}'
        if context['when'] == 'present':
            update += f" {action} {object} {when_helper}"
        else:
            update += f" {when_helper} {action} {object}"

        if context['when'] == 'future':
            update = f"{random.choice(ANTICIPATION_PREFIXES)} {update} and {context['what']['anticipation']}"
        elif context['when'] == 'present':
            update = f"{random.choice(CURRENT_PREFIXES)} {update}"
        elif context['when'] == 'past':
            update = f"{random.choice(REACTION_PREFIXES)} {update} and now {context['what']['reaction']}"

        cache.set("bbot", json.dumps(context))
        update = " ".join(update.split())
        return update


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


class ESPNBroker():

    def call_espn(self, view=None):
        cookies = {"swid": "{ADB2C88A-0CCD-4491-B8B7-4657E6A412FD}",
                   "espn_s2": "AECvR2KuFAHIFNvXPmowC7LgFu4G2jj6tzWOaOd8xnX2wu3BaSy3Dogb5KU0KAiHu3xcqKzkMa%2FwbLIIzA4DMqtr"
                              "%2FZF48XsPMFyOGScz3xl0qO3ekELFD7qgY0qYdGbg%2BwbX0NntqxWwPaLPdrEaIc1vlXxehme7cbLRq6Uf5iP3f%"
                              "2FpQvG51KexkEMJy6Hc1C1zZxZ41fQ4EddVA%2BhaqQ9%2BADWELwT9hFbPFjoBxco8T%2FvSxS0TJFEqLiBUBfp%2"
                              "F2RbE%3D"}

        url = ESPN_URL

        r = requests.get(url, cookies=cookies, params={'view': view})
        return r.json()

    def get_rostered_players(self):
        rostered_players = {}
        response = self.call_espn(view='mRoster')
        for team in response['teams']:
            for player in team['roster']['entries']:
                lookup = player['playerPoolEntry']['player']['lastName'].lower()
                rostered_players[lookup] = {
                    'full_name': player['playerPoolEntry']['player']['fullName'].lower()
                }

