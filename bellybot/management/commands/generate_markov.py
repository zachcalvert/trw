"""Generate random chat messages via a markov chain churning through every message ever sent in the GroupMe """
import json
import random

from django.core.management.base import BaseCommand, CommandError

from groupme_messages import MESSAGES


with open('trigram_to_trigram_model.json') as f:
    model = json.load(f)


class Command(BaseCommand):
    help = "blah"  # noqa: Django required

    def markov_respond(self, message):
        last_three = ' '.join(message.split()[-3:])
        response = []

        sentence_length = random.choice(range(3, 15))
        for i in range(sentence_length):
            try:
                phrase = random.choice(model["trigram_model"][last_three])
            except KeyError:
                return None

            response.append(phrase)
            last_three = phrase

        return ' '.join(response)

    def handle(self, *args, **options):

        for i in range(1000):
            message = random.choice(MESSAGES).lower()
            print(self.markov_respond(message))
