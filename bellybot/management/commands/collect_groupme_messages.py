""" A one time script (hopefully) to collect and store historical messages sent """
from collections import defaultdict
import json
import requests
import time

import spacy

from django.core.management.base import BaseCommand, CommandError

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")

BASE_URL = "https://api.groupme.com/v3/"
GROUP_ID = "16191637"
TOKEN = "kUtmZNokfpZvOE8KrOw1tb7cF15wZ3h55Vxk0T34"


class Command(BaseCommand):
    help = "Collects messages sent within a given groupme group"  # noqa: Django required

    def handle(self, *args, **options):

        starting_message_id = None
        groupme_messages = []
        for i in range(312):

            messages_url = f"{BASE_URL}groups/{GROUP_ID}/messages?token={TOKEN}&limit=100"

            if starting_message_id:
                messages_url += f"&before_id={starting_message_id}"

            response = requests.get(messages_url)

            if response.status_code == 200:
                content = json.loads(response.content.decode())
                message_list = content['response']['messages']

                for message in message_list:
                    if message['sender_type'] != 'bot' and message['text']:
                        groupme_messages.append('{}'.format(message['text'].lower().replace('\n', '')))

                    try:
                        next_message = message_list[message_list.index(message) + 1]
                    except IndexError:
                        starting_message_id = message['id']
                        continue

            else:
                print(response)

            print('retrieved {} out of 500 batches'.format(i))

        print(groupme_messages)

        # with open('groupme_messages.json') as f:
        #     groupme_messages = json.load(f)

        # tokenize each message in the list
        tokens = []
        for count, groupme_message in enumerate(groupme_messages):
            print(f'tokenizing message {count}')
            tokens.extend(nlp(groupme_message))

        model = defaultdict(list)
        for count, token in enumerate(tokens):
            print(f'adding token {count} to model')
            try:
                key = ' '.join([str(tokens[count]), str(tokens[count+1]), str(tokens[count+2])])
                model[key].append(' '.join([str(tokens[count+3]), str(tokens[count+4]), str(tokens[count+5])]))
            except IndexError:
                pass

        print(model)
        model_json = {"trigram_model": model}

        with open('trigram_to_trigram_model.json', 'w') as f:
            json.dump(model_json, f)
