import random

from bellybot.vocab.actions import PREPOSITIONS, PAST_ACTIONS
from bellybot.vocab.emojis import EMOJIS
from bellybot.vocab.names import NAMES
from bellybot.vocab.objects import OBJECTS, ARTICLES
from bellybot.vocab.places import PLACES
from bellybot.vocab.prefixes import PREFIXES
from bellybot.vocab.reasons import REASONS
from bellybot.vocab.suffixes import SUFFIXES
from bellybot.vocab.times import TIMES

STOCK_ANSWERS = [
    'why would I know that',
    'hmm thats bordering on impossible for me to answer',
    'i straight up dont know',
    'not sure about that one',
    'idk',
    'sorry bb im too high rn',
    'i havent been trained to answer that'
]

AMOUNTS = [
    'nothing',
    'everything',
    'shit',
    'shit all',
    'absolutely nothing'
]


class Answerer(object):

    def __init__(self, sender, message):
        self.sender = sender
        self.message = message
        self.trigger = next((phrase for phrase in QUESTION_SWITCHER.keys() if phrase in message), None)

    @staticmethod
    def is_question(message):
        return next((phrase for phrase in QUESTION_SWITCHER.keys() if phrase in message), None) is not None

    def answer(self):
        fn = QUESTION_SWITCHER[self.trigger]
        try:
            return fn(self)
        except Exception:
            return random.choice(STOCK_ANSWERS)

    def _build_answer(self, prefix=True, core=None, suffix=True, emojis=True):
        answer = ''

        if prefix:
            answer += f'{random.choice(PREFIXES)} ' if random.choice([1, 2]) == 2 else ''
        if core:
            answer += '{}'.format(core)
            answer += '! ' if random.choice([1, 2]) == 1 else '. '
        if suffix:
            answer += f'{random.choice(SUFFIXES)} ' if random.choice([1, 2]) == 2 else ''
        if emojis:
            if random.choice([1, 3]) == 1:
                n = random.choice([1, 2, 3, 4])
                emojis = ' '.join(random.sample(EMOJIS, n))
                answer += ' {}'.format(emojis)

        # remove any duplicate spaces
        answer = " ".join(answer.split())

        return answer


    def _make_subject_swaps(self, core):

        return core.replace(' my ', ' your ')\
            .replace(' mine ', ' yours ')\
            .replace(' me ', ' you ')\
            .replace('bbot', '')\
            .replace(' i ', ' you ')

    def how(self):
        core = f'{random.choice(NAMES)} {random.choice(PAST_ACTIONS)} {random.choice(PREPOSITIONS)} ' \
               f'{random.choice(ARTICLES)} {random.choice(OBJECTS)}'

        return self._build_answer(prefix=True, core=core, suffix=True, emojis=True)

    def what(self):
        return

    def when(self):
        core = '{} {}'.format(random.choice(TIMES), self.sender)
        return self._build_answer(prefix=True, core=core, suffix=True, emojis=True)

    def where(self):
        core = '{}'.format(random.choice(PLACES))
        return self._build_answer(prefix=True, core=core, suffix=True, emojis=True)

    def who(self):
        if 'waiver' in self.message:
            pass
        core = '{}'.format(random.choice(NAMES))
        return self._build_answer(prefix=True, core=core, suffix=True, emojis=True)

    def why(self):
        _, question = self.message.split('why')
        core, _ = question.split('?', 1)

        core = 'because' if random.choice([1, 2]) == 2 else 'cause'
        core += ' {} {}'.format(random.choice(NAMES), random.choice(REASONS))

        return self._build_answer(prefix=True, core=core, suffix=True, emojis=True)

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
        core = '{}{} i wanna {}{}'.format(self.sender, first_punc, negate, core)
        return self._build_answer(prefix=True, core=core, suffix=True, emojis=True)


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
    'wanna': Answerer.wanna
}
