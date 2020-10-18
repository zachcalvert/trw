""" A one time script (hopefully) to collect and store historical messages sent """
import random

from django.core.management.base import BaseCommand, CommandError

from bellybot.models import GroupMeBot
from groupme_messages import MESSAGES


class Command(BaseCommand):
    help = "blah"  # noqa: Django required

    def handle(self, *args, **options):

        for i in range(1000):
            message = random.choice(MESSAGES).lower()
            print(GroupMeBot().markov_respond('zach', message))