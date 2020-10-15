import json
import random
import requests

import giphy_client
from giphy_client.rest import ApiException

from bellybot.phrases import BB_PHRASES

giphy_api_instance = giphy_client.DefaultApi()

ESPN_URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2020/segments/0/leagues/832593"
GROUPME_URL = "https://api.groupme.com/v3/bots/post"
GIS_ID = "cc646ee172e69377d"
GIPHY_API_KEY = "qUzMZY2GSYY8y"
GOOGLE_SEARCH_API_KEY = "AIzaSyCknrR34a7r"


class GroupMeBot:

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

    def respond(self, sender, message):
        response = None
        image = None

        message = message.lower()

        if message.startswith('bb '):
            _, command = message.split('bb ')

            if command.startswith('speak'):
                response = random.choice(BB_PHRASES)

            elif command.startswith('image '):
                _, search_terms = message.split('bb image ')
                response = search_terms

                success, image = image_search(search_terms)
                if not success:
                    response = f"I had trouble image searching '{search_terms}', sorry!"
            elif command.startswith('gif '):
                _, search_terms = message.split('bb gif ')
                success, gif = gif_search(search_terms)
                if not success:
                    response = f"I had trouble gif searching '{search_terms}', sorry!"
                else:
                    response = gif
            else:
                response = f"sorry {sender}, I didn't understand that"

        elif 'salt' in message:
            success, image = image_search('so salty')
            response = "someone feeling salty?"
        elif 'commercial' in message:
            response = "We don't do commercials in the pit!"
        elif 'shotgun' in message:
            success, gif = gif_search('beer shotgun')
            if success:
                response = gif
        elif 'strikeout' in message:
            success, gif = gif_search('beer strikeout')
            if success:
                response = gif
        elif 'ducks' in message:
            success, image = image_search('go ducks!')
            response = "SCO"
        elif 'ibm ' in message or 'watson' in message:
            response = "IBM's Watson is a steaming pile of shit"

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
    gif = api_response.data[index]
    url = gif.images.downsized_large.url
    return True, url