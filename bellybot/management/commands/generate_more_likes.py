from django.core.management.base import BaseCommand, CommandError

from bellybot.vocab.rostered_players import NFL_PLAYERS


class Command(BaseCommand):
    help = "blah"  # noqa: Django required

    def handle(self, *args, **options):
        user_input = ''
        more_likes = {}

        for player, pd in NFL_PLAYERS.items():
            more_likes[pd['full_name']] = []

        for player in more_likes.keys():
            print('{}? more like: '.format(player))
            user_input = input()
            if user_input != 'n' and user_input not in more_likes[player]:
                more_likes[player].append(user_input)

        print(more_likes)


