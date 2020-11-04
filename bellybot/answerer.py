import json
import os
import random

import redis

from bellybot import Responder

from bellybot.context.people import ALL_PEOPLE
from bellybot.context.places import PLACES
from bellybot.context.reactions import EMOTIONS

from bellybot.vocab import YESES
from bellybot.vocab.adverbs import ADVERBS
from bellybot.vocab.emojis import EMOJIS, LAUGHING
from bellybot.vocab.rostered_players import NFL_PLAYERS
from bellybot.vocab.suffixes import SUFFIXES
from bellybot.vocab.times import TIMES

from team_names import TEAM_NAMES

redis_host = os.environ.get('REDISHOST', 'localhost')
cache = redis.StrictRedis(host=redis_host, port=6379)


class Answerer(Responder):

    def __init__(self, sender, message):
        super().__init__()
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
            answer = fn(self)
            self.send_message(answer)
        except Exception:
            answer = self.get_update()

        return answer

    def _build_answer(self, confirm=True, core=None, suffix=True, emojis=True, exclamation=True, laughing=False):
        answer = ''

        laughs = {'lol', 'lmao', 'haha', 'lmfao'}
        if any(laugh in self.message for laugh in laughs):
            laughing = True

        if confirm:
            answer += f'{random.choice(YESES)} ' if random.choice([1, 2]) == 2 else ''
        if core:
            answer += '{}'.format(core)
            answer += '! ' if random.choice([1, 2]) == 1 and exclamation else '. '
        if suffix:
            answer += f'{random.choice(SUFFIXES)} ' if random.choice([1, 2]) == 2 else ''
        if emojis:
            if random.choice([1,2]) == 1:
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
            .replace('yours', 'mine')\
            .replace('you', 'me')\
            .replace('your', 'my')\
            .replace('though', '')\
            .replace('yet', '')

    def hedge(self):
        first = ['lol', 'well', '', '']
        second = ['shit', 'damn', 'dang', '', '', '']
        third = ['man', 'dude', 'bro', 'my guy']
        puncs = ['.', ',', '!' '!!']
        fourth = ['idk', 'i dont know', 'i got no idea', 'couldnt possibly say', 'couldn\'t tell ya', 'no idea',
                  'wish i could say', 'i honestly don\'t know', 'honestly got no idea']

        return '{} {} {}{} {}'.format(
            random.choice(first),
            random.choice(second),
            random.choice(third),
            random.choice(puncs),
            random.choice(fourth)
        )

    def get_update(self):
        update = random.choice(EMOTIONS['positive'])
        return self._build_answer(confirm=False, core=update, suffix=True, emojis=True)

    def is_checkin(self, message):
        message = message.replace("'", "").replace(" ", "")
        if any(checkin in message for checkin in ['howare', 'howsitgoin', 'howsyourday', 'howwedoin', 'whatsgood', 'whatup', 'whatsgoin', 'whatsnew']):
            return True
        return False

    def how(self):
        if self.is_checkin(self.message):
            return self.get_update()

        if 'nickname' in self.message:
            return self.nickname()

        core = self.hedge()
        return self._build_answer(confirm=False, core=core, suffix=True, emojis=True)

    def what(self):
        if self.is_checkin(self.message):
            return self.get_update()

        core = self.hedge()
        return self._build_answer(confirm=False, core=core, suffix=True, emojis=True)

    def when(self):
        core = '{}'.format(random.choice(TIMES))
        return self._build_answer(confirm=False, core=core, suffix=True, emojis=True)

    def where(self):
        core = '{}'.format(random.choice(PLACES))
        return self._build_answer(confirm=False, core=core, suffix=True, emojis=True)

    def who(self):
        if 'who\'s there' in self.message or 'is there' in self.message:
            try:
                context = json.loads(cache.get("bbot"))
                core = ' '.join(context['who'])
            except (KeyError):
                core = 'its just me lol'
        elif 'favorite team' in self.message:
            core = 'the lions'
        elif ' win ' in self.message:
            core = self.hedge()
        else:
            core = '{}'.format(random.choice(ALL_PEOPLE))

        return self._build_answer(confirm=False, core=core, suffix=True, emojis=True)

    def why(self):
        core = self.hedge()
        return self._build_answer(confirm=False, core=core, suffix=True, emojis=True)

    def are_you(self):
        if 'how are you' in self.message:
            return self.get_update()
        return self._build_answer(confirm=True, core=None, suffix=True, emojis=True)

    def did_you(self):
        return self._build_answer(confirm=True, core=None, suffix=True, emojis=True)

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
        return self._build_answer(confirm=True, core=None, suffix=True, emojis=True, laughing=True)

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
        try:
            new_nickname = TEAM_NAMES.pop()
            response = '{}, your new nickname is {}'.format(self.sender, new_nickname)
        except IndexError:
            response = self.hedge()
        return response

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

    def right(self):
        choices = ['fucking right', 'damn straight', 'that\'s right']
        core = '{} {}'.format(random.choice(choices), self.sender)
        return self._build_answer(confirm=False, core=core, suffix=True, emojis=True)

    def chyaa(self):
        chya = 'chya' + 'a'*random.choice([2,3,4,5,6,7,8])
        core = '{} {}'.format(chya, self.sender)
        return self._build_answer(confirm=False, core=core, suffix=True, emojis=True)

    def eyaww(self):
        eyaw = 'eyaw' + 'w'*random.choice([2,3,4,5,6,7,8])
        core = '{}!'.format(eyaw)
        return self._build_answer(confirm=False, core=core, suffix=True, emojis=True)

    def good_morning(self):
        good = 'g' + 'o'*random.choice([2,3,4,5]) + 'd'
        core = '{} morning {}!'.format(good, self.sender)
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
    'right bbot?': Answerer.right,
    'chyaa': Answerer.chyaa,
    'eyaww': Answerer.eyaww,
    'good morning': Answerer.good_morning,
    'want a': Answerer.wanna,
    'want to': Answerer.wanna
}
