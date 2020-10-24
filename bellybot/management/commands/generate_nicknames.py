""" Collect all the named_entities ever sent """
import json
import random
import spacy

from django.core.management.base import BaseCommand

from bellybot.vocab.named_entities import ENTITIES as named_entities

nlp = spacy.load("en_core_web_sm")

BASE_URL = "https://api.groupme.com/v3/"
GROUP_ID = "16191637"
TOKEN = "kUtmZNokfpZvOE8KrOw1tb7cF15wZ3h55Vxk0T34"


class Command(BaseCommand):
    help = "Collects messages sent within a given groupme group"  # noqa: Django required

    def handle(self, *args, **options):
        random.shuffle(named_entities)

        with open('nicknames.json') as json_file:
            existing_nicknames = json.load(json_file)
        nicknames = set(existing_nicknames["nicknames"])

        for i in range(100):
            potential = '{} {}'.format(named_entities.pop(), named_entities.pop())
            print('{}'.format(potential))
            user_input = input()
            if user_input == 'l':
                nicknames.add(potential)

        new_nicknames = {"nicknames": list(nicknames)}
        print(new_nicknames)

        with open('nicknames.json', 'w') as f:
            json.dump(new_nicknames, f)