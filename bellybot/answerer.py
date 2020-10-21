import random

from bellybot.vocab.actions import PAST_ACTIONS, ONGOING_ACTIONS, INFINITIVE_ACTIONS
from bellybot.vocab.adverbs import ADVERBS
from bellybot.vocab.emojis import EMOJIS, LAUGHING
from bellybot.vocab.emotions import EMOTIONS
from bellybot.vocab.jokes import JOKES
from bellybot.vocab.names import NAMES
from bellybot.vocab.places import PLACES
from bellybot.vocab.prefixes import PREFIXES
from bellybot.vocab.reactions import REACTIONS
from bellybot.vocab.reasons import REASONS
from bellybot.vocab.rostered_players import NFL_PLAYERS
from bellybot.vocab.stallers import STALLERS
from bellybot.vocab.suffixes import SUFFIXES
from bellybot.vocab.times import TIMES
from team_names import TEAM_NAMES

AMOUNTS = [
    'nothing',
    'everything',
    'shit',
    'shit all',
    'absolutely zero',
    'everything',
]


class Answerer(object):

    def __init__(self, sender, message, player=None):
        self.sender = sender
        self.message = message
        self.trigger = next((phrase for phrase in QUESTION_SWITCHER.keys() if phrase in message), None)
        self.player = player

    @staticmethod
    def is_question(message):
        return next((phrase for phrase in QUESTION_SWITCHER.keys() if phrase in message), None) is not None

    def answer(self):
        fn = QUESTION_SWITCHER[self.trigger]
        try:
            return fn(self)
        except Exception:
            return self.make_excuse()

    def _build_answer(self, prefix=True, core=None, suffix=True, emojis=True, exclamation=True, laughing=False):
        answer = ''

        if prefix:
            answer += f'{random.choice(PREFIXES)} ' if random.choice([1, 2]) == 2 else ''
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

    def make_excuse(self):
        past = [
            'just',
            'just now',
        ]
        current = [
            'right now',
            'right now',
            'now',
            'now',
            'at the moment',
            'currently',
            'presently'
        ]
        future = [
            'just said hes gonna',
            'is about to',
            'is setting up to',
            'is getting ready to',
            'is saying he\'s gonna',
            'is saying he\'s about to',
            'is threatening to',
            'is prepping to',
            'is fixing to',
        ]

        # note the reverse order for current! or dont :)
        whens = {
            'past': (past, PAST_ACTIONS),
            'current': (ONGOING_ACTIONS, current),
            'future': (future, INFINITIVE_ACTIONS)
        }
        when = whens[random.choice(['past', 'current', 'future'])]
        excuse = f'{random.choice(NAMES)} {random.choice(when[0])} {random.choice(when[1])}'

        excuse += f' and {random.choice(REACTIONS)}'
        core = '{} {}'.format(random.choice(STALLERS), excuse)
        return self._build_answer(prefix=False, core=core, suffix=False, emojis=False, exclamation=False)

    def how(self):
        if 'are you' in self.message:
            core = 'im {}'.format(random.choice(EMOTIONS))
            return self._build_answer(prefix=True, core=core, suffix=True, emojis=True)
        else:
            return self.make_excuse()

    def what(self):
        return self.make_excuse()

    def when(self):
        core = '{} {}'.format(random.choice(TIMES), self.sender)
        return self._build_answer(prefix=False, core=core, suffix=True, emojis=True)

    def where(self):
        core = '{}'.format(random.choice(PLACES))
        return self._build_answer(prefix=False, core=core, suffix=True, emojis=True)

    def who(self):
        if 'waiver' in self.message:
            pass
        if 'favorite team' in self.message:
            core = 'the lions'
        else:
            core = '{}'.format(random.choice(NAMES))

        return self._build_answer(prefix=False, core=core, suffix=True, emojis=True)

    def why(self):
        _, question = self.message.split('why')
        core, _ = question.split('?', 1)

        core = 'because' if random.choice([1, 2]) == 2 else 'cause'
        core += ' {} {}'.format(random.choice(NAMES), random.choice(REASONS))

        return self._build_answer(prefix=False, core=core, suffix=True, emojis=True)

    def are_you(self):
        _, question = self.message.split('are you')
        core, _ = question.split('?', 1)

        if core:
            core = self._make_subject_swaps(core)
            if 'gonna do' in core:
                core = core.replace('gonna do', 'gonna do {}'.format(random.choice(AMOUNTS)))

        negate = 'not' if random.choice([1, 2]) == 1 else ''
        core = '{} i am {}{}'.format(self.sender, negate, core)

        return self._build_answer(prefix=True, core=core, suffix=True, emojis=True)

    def did_you(self):
        _, question = self.message.split('did you')
        core, _ = question.split('?', 1)

        if core:
            core = self._make_subject_swaps(core)

        core = '{} i did{}'.format(self.sender, core)
        return self._build_answer(prefix=True, core=core, suffix=True, emojis=True)

    def do_you(self):
        _, question = self.message.split('do you')
        core, _ = question.split('?', 1)

        if core:
            core = self._make_subject_swaps(core)

        core = '{} i do{}'.format(self.sender, core)
        return self._build_answer(prefix=True, core=core, suffix=True, emojis=True)

    def have_you(self):
        _, question = self.message.split('have you')
        core, _ = question.split('?', 1)

        if core:
            if core.startswith(' ever'):
                core = core.replace(' ever', '')
            core = self._make_subject_swaps(core)

        negate = 'not' if random.choice([1, 2]) == 1 else ''
        core = '{} i have {}{}'.format(self.sender, negate, core)

        return self._build_answer(prefix=True, core=core, suffix=True, emojis=True)

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

        negate = 'not' if random.choice([1, 2]) == 1 else ''
        core = '{} {} {}{}'.format(self.sender, random.choice(list(conjugations.values())), negate, core)
        return self._build_answer(prefix=True, core=core, suffix=True, emojis=True)

    def wanna(self):
        _, question = self.message.split('wanna')
        core, _ = question.split('?', 1)

        if core:
            core = self._make_subject_swaps(core)

        negate = 'not' if random.choice([1, 2]) == 1 else ''
        first_punc = '!' if random.choice([1, 2]) == 1 else '.'
        adverb = random.choice(ADVERBS) if random.choice([1, 2]) == 1 else ''
        core = '{}{} i {} wanna {}{}'.format(self.sender, first_punc, adverb, negate, core)
        return self._build_answer(prefix=True, core=core, suffix=True, emojis=True)

    def nickname(self):
        if 'new nickname' in self.message or 'another nickname' in self.message:
            new_nickname = TEAM_NAMES.pop()
            response = 'ok {}, your new nickname is {}'.format(self.sender, new_nickname)
            return response
        else:
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
        if self.player:
            player = self.player
        else:
            player = random.choice(list(JOKES.keys()))
        try:
            core = '{}? more like {}!'.format(player, JOKES[player].pop())
        except IndexError:
            return None

        core += ' roasted' if random.choice([1,2,3]) == 1 else ''
        return self._build_answer(prefix=False, core=core, suffix=False, emojis=False, laughing=True)


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
}
