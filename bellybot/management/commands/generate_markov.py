"""Generate random chat messages via a markov chain churning through every message ever sent in the GroupMe """
import random

from django.core.management.base import BaseCommand, CommandError

from groupme_messages import MESSAGES


class Command(BaseCommand):
    help = "blah"  # noqa: Django required

    def markov_respond(self, message):
        last_two = ' '.join(message.split()[-2:])
        response = []

        sentence_length = random.choice(range(6, 15))
        for i in range(sentence_length):
            try:
                phrase = random.choice(model["bigram_model"][last_two])
            except KeyError:
                break

            response.append(phrase)
            last_two = phrase

        return ' '.join(response)

    def handle(self, *args, **options):

        for i in range(1000):
            message = random.choice(MESSAGES).lower()
            print(self.markov_respond(message))
