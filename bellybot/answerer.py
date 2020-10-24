import json
import os
import random

import redis

from bellybot.context.actions import ACTIONS
from bellybot.context.people import ALL_PEOPLE
from bellybot.context.places import PLACES
from bellybot.context.reactions import ANTICIPATION_PREFIXES, ANTICIPATIONS, REACTION_PREFIXES, REACTIONS, CURRENT_PREFIXES
from bellybot.context.times import TIME_CONTEXTS

from bellybot.vocab import YESES
from bellybot.vocab.adverbs import ADVERBS
from bellybot.vocab.emojis import EMOJIS, LAUGHING
from bellybot.vocab.rostered_players import NFL_PLAYERS
from bellybot.vocab.suffixes import SUFFIXES
from bellybot.vocab.times import TIMES

from team_names import TEAM_NAMES

redis_host = os.environ.get('REDISHOST', 'localhost')
cache = redis.StrictRedis(host=redis_host, port=6379)


class Answerer(object):

    def __init__(self, sender, message):
        self.sender = sender
        self.message = message
        self.trigger = next((phrase for phrase in QUESTION_SWITCHER.keys() if phrase in message), None)
        self.player = self.get_player()

    @staticmethod
    def should_answer(message):
        return next((phrase for phrase in QUESTION_SWITCHER.keys() if phrase in message), None) is not None

    def answer(self):
        fn = QUESTION_SWITCHER[self.trigger]
        try:
            return fn(self)
        except Exception:
            return self.give_update()

    def _build_answer(self, confirm=True, core=None, suffix=True, emojis=True, exclamation=True, laughing=False):
        answer = ''

        if confirm:
            answer += f'{random.choice(YESES)} ' if random.choice([1, 2]) == 2 else ''
        if core:
            answer += '{}'.format(core)
            answer += '! ' if random.choice([1, 2]) == 1 and exclamation else '. '
        if suffix:
            answer += f'{random.choice(SUFFIXES)} ' if random.choice([1, 2]) == 2 else ''
        if emojis:
            if random.choice([1, 3]) == 1:
                n = random.choice([1, 1, 2])
                emojis = ' '.join(random.sample(EMOJIS, n))
                answer += ' {}'.format(emojis)
        if laughing:
            n = random.choice([1, 2, 3])
            emojis = ' '.join(random.sample(LAUGHING, n))
            answer += ' {}'.format(emojis)

        answer = " ".join(answer.split())  # remove any duplicate spaces
        return answer

    def _make_subject_swaps(self, core):
        return core.replace(' my ', ' your ')\
            .replace(' mine ', ' yours ')\
            .replace(' me ', ' you ')\
            .replace('bbot', '')\
            .replace(' i ', ' you ')\
            .replace('your', 'my')\
            .replace('though', '')\
            .replace('yet', '')

    def _increment_time(self, when):
        times = list(TIME_CONTEXTS.keys())
        new_time = times[times.index(when) + 1]
        return new_time

    def create_context(self):
        subject = random.choice(ALL_PEOPLE)
        action = random.choice(list(ACTIONS.keys()))
        object = random.choice(ACTIONS[action]['objects'])
        location = random.choice(PLACES)

        bbot_context = {
            "who": ["me", subject, random.choice(ALL_PEOPLE)],
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
        cache.set("bbot", json.dumps(bbot_context))
        return bbot_context

    def give_update(self):
        try:
            context = json.loads(cache.get("bbot"))
            context['when'] = self._increment_time(context['when'])
        except (TypeError, IndexError):
            context = self.create_context()

        subject = context['what']['subject']
        when_helper = random.choice(TIME_CONTEXTS[context['when']])
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
            update = f"{random.choice(REACTION_PREFIXES)} {update} and {context['what']['reaction']}"

        cache.set("bbot", json.dumps(context))
        update = " ".join(update.split())
        return update

    def how(self):
        if 'nickname' in self.message:
            return self.nickname()
        return self.give_update()

    def what(self):
        return self.give_update()

    def when(self):
        core = '{} {}'.format(random.choice(TIMES), self.sender)
        return self._build_answer(confirm=False, core=core, suffix=True, emojis=True)

    def where(self):
        if 'where are you' in self.message:
            context = json.loads(cache.get("bbot"))
            core = context['where']
        else:
            core = '{}'.format(random.choice(PLACES))
        return self._build_answer(confirm=False, core=core, suffix=True, emojis=True)

    def who(self):
        if 'who\'s there' in self.message or 'is there' in self.message:
            try:
                context = json.loads(cache.get("bbot"))
                core = ' '.join(context['who'])
            except (KeyError):
                pass
        elif 'favorite team' in self.message:
            core = 'the lions'
        else:
            core = '{}'.format(random.choice(ALL_PEOPLE))

        return self._build_answer(confirm=False, core=core, suffix=True, emojis=True)

    def why(self):
        return self.give_update()

    def are_you(self):
        if 'how are you' in self.message:
            return self.give_update()

        _, question = self.message.split('are you')
        core, _ = question.split('?', 1)

        if core:
            core = self._make_subject_swaps(core)
            if 'gonna do' in core:
                core = core.replace('gonna do', 'gonna do something')

        negate = 'not' if random.choice([1, 2]) == 1 else ''
        core = '{} i am {}{}'.format(self.sender, negate, core)

        return self._build_answer(confirm=True, core=core, suffix=True, emojis=True)

    def did_you(self):
        _, question = self.message.split('did you')
        core, _ = question.split('?', 1)

        if core:
            core = self._make_subject_swaps(core)

        core = '{} i did{}'.format(self.sender, core)
        return self._build_answer(confirm=True, core=core, suffix=True, emojis=True)

    def do_you(self):
        _, question = self.message.split('do you')
        core, _ = question.split('?', 1)

        if core:
            core = self._make_subject_swaps(core)

        core = '{} i do{}'.format(self.sender, core)
        return self._build_answer(confirm=True, core=core, suffix=True, emojis=True)

    def have_you(self):
        _, question = self.message.split('have you')
        core, _ = question.split('?', 1)

        if core:
            if core.startswith(' ever'):
                core = core.replace(' ever', '')
            core = self._make_subject_swaps(core)

        negate = 'not' if random.choice([1, 2]) == 1 else ''
        core = '{} i have {}{}'.format(self.sender, negate, core)

        return self._build_answer(confirm=True, core=core, suffix=True, emojis=True)

    def will_you(self):
        conjugations = {
            1: 'ill',
            2: 'i\'ll',
            3: 'i will',
        }

        _, question = self.message.split('will you')
        core, _ = question.split('?', 1)

        if core:
            if core.startswith(' ever'):
                core = core.replace(' ever', '') if random.choice([1, 2]) == 1 else ' never'
            if core.startswith(' please'):
                core = core.replace(' please', '')
            core = self._make_subject_swaps(core)

        core = '{} {} {}'.format(self.sender, random.choice(list(conjugations.values())), core)
        return self._build_answer(confirm=True, core=core, suffix=True, emojis=True)

    def wanna(self):
        _, question = self.message.split('wanna')
        core, _ = question.split('?', 1)

        if core:
            core = self._make_subject_swaps(core)

        first_punc = '!' if random.choice([1, 2]) == 1 else '.'
        adverb = random.choice(ADVERBS) if random.choice([1, 2]) == 1 else ''
        core = '{}{} i {} wanna {}'.format(self.sender, first_punc, adverb, core)
        return self._build_answer(confirm=True, core=core, suffix=True, emojis=True)

    def nickname(self):
        if 'new nickname' in self.message or 'another nickname' in self.message:
            new_nickname = TEAM_NAMES.pop()
            response = 'ok {}, your new nickname is {}'.format(self.sender, new_nickname)
            return response
        else:
            return None

    def get_player(self):
        for player in NFL_PLAYERS.keys():
            if player in self.message:
                return NFL_PLAYERS[player]['full_name']
        return None

    def go_lions(self):
        lions = [
            'calvin johnson',
            'barry sanders',
            'charlie batch lions',
            'matt stafford',
            'detroit lions',
            'go detroit lions',
            'detroit lions',
        ]
        return random.choice(lions)

    def joke(self):
        return self.give_update()

    def right(self):
        core = 'fucking right {}!'.format(self.sender)
        return self._build_answer(confirm=False, core=core, suffix=True, emojis=True)


QUESTION_SWITCHER = {
    'how': Answerer.how,
    'what': Answerer.what,
    'when': Answerer.when,
    'where': Answerer.where,
    'who': Answerer.who,
    'why': Answerer.why,
    'are you': Answerer.are_you,
    'did you': Answerer.did_you,
    'do you': Answerer.do_you,
    'have you': Answerer.have_you,
    'will you': Answerer.will_you,
    'wanna': Answerer.wanna,
    'nickname': Answerer.nickname,
    'joke': Answerer.joke,
    'right bbot?': Answerer.right,
}
