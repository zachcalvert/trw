import random

from bellybot.data.names import NAMES
from bellybot.data.reasons import REASONS
from bellybot.data.times import TIMES

STOCK_ANSWERS = [
    'why would I know that',
    'hmm thats bordering on impossible to answer',
    'i dont fucking know man',
    'not sure about that one',
    'idk',
]

AMOUNTS = [
    'nothing',
    'everything',
    'shit'
]

PREFIXES = [
    'yea',
    'yes',
    'yeah',
    'yaw',
    'hell yea',
    'fuck yea',
    'for sure',
    'definitely',
    'absolutely',
    'actually',
    'um yea',
    'uh yea',
    'uh ya',
    'um of course'
    'lol',
    'lol',
    'lmao',
    'yea',
    'yea',
    'ok',
    'okay',
    'alright',
    'sounds good',
    'right on',
    'of course',
    'fucking right',
    'yupp',
    'yup',
    'honestly'
]

EXPLANATION_STARTERS = [
    'maybe',
    'probably',
    'i think',
    'likely',
    'not certain but',
    'not 💯 on this but',
    'most likely ',
    '',
    '',
]

BECAUSES = ['because', 'because', 'cause', 'cause', 'since']

SUFFIXES = [
    'lets gooooo!',
    'lol my bad',
    'lol',
    'it gets better',
    'better get that ass',
    'can you get out of my ass',
    'now get out',
    'we gucci',
    'we lit',
    'we lit!',
    'we litty gurl',
    'wmflg',
    'lets shotgun',
    'id bet on that',
    'you sound salty lol',
    'broo',
    'bro.',
    'my bro',
    'my good bitch',
    'in the old ass',
    'but why',
    'king!',
    'it slaps',
    'lets go!',
    'flames',
    'we flames',
    'so yea',
    'fuck!',
    'stupid little flamer',
    'stupid little riccy',
    'flamer!!',
    'lmao',
    'lmao',
    'fuckin lmao',
    'lol',
    'lolll',
    'fuckin lol',
    'loll',
    'bish',
    'ya bish',
    'botch',
    'batchley',
    'fuckin lol dude',
    'fuckin lol',
    'we slap',
]

EMOJIS = [
    '😂',
    '😂',
    '😂',
    '🤣',
    '🤣',
    '🤣',
    '😎',
    '😎',
    '😎',
    '🔥',
    '🔥',
    '🧀',
    '🧀',
    '👏',
    '👏',
    '🌊',
    '🌊',
    '💯',
    '💯',
    '🙀',
    '🙀',
    '😘',
    '😘',
    '😟',
    '😳',
    '🍆',
    '🍆',
    '🏌',
    '🤤',
    '🤤',
]


class Answerer:

    def how(self, sender, message):
        return

    def what(self, sender, question):
        return

    @staticmethod
    def when(sender, question):
        answer = ''
        if random.choice([1, 2]) == 1:
            answer += '{} '.format(random.choice(EXPLANATION_STARTERS))

        answer += '{} {}.'.format(random.choice(TIMES), sender)

        if random.choice([1, 2]) == 1:
            answer += (' {}'.format(random.choice(SUFFIXES)))

        if random.choice([1, 3]) == 1:
            n = random.choice([1, 2, 3, 4])
            emojis = ' '.join(random.sample(EMOJIS, n))
            answer += ' {}'.format(emojis)

        return answer

    def where(self, sender, question):
        pass

    @staticmethod
    def who(sender, question):
        answer = ''
        if random.choice([1, 2]) == 1:
            answer += '{} '.format(random.choice(EXPLANATION_STARTERS))

        answer += '{}.'.format(random.choice(NAMES))

        if random.choice([1, 2]) == 1:
            answer += (' {}'.format(random.choice(SUFFIXES)))

        if random.choice([1, 3]) == 1:
            n = random.choice([1, 2, 3, 4])
            emojis = ' '.join(random.sample(EMOJIS, n))
            answer += ' {}'.format(emojis)

        return answer

    @staticmethod
    def why(sender, message):
        _, question = message.split('why')
        core, _ = question.split('?', 1)

        answer = ''
        if random.choice([1, 2]) == 1:
            answer += '{} '.format(random.choice(EXPLANATION_STARTERS))
        answer += random.choice(BECAUSES)

        answer += ' {} {}'.format(random.choice(NAMES), random.choice(REASONS))

        answer += '! ' if random.choice([1, 2]) == 1 else '. '

        if random.choice([1, 2]) == 1:
            answer += (' {}'.format(random.choice(SUFFIXES)))

        if random.choice([1, 3]) == 1:
            n = random.choice([1,2,3,4])
            emojis = ' '.join(random.sample(EMOJIS, n))
            answer += ' {}'.format(emojis)

        return answer

    @staticmethod
    def are_you(sender, message):
        _, question = message.split('are you')
        core, _ = question.split('?', 1)

        if core:
            core = make_subject_swaps(core)
            if 'gonna do' in core:
                core = core.replace('gonna do', 'gonna do {}'.format(random.choice(AMOUNTS)))

        answer = ''

        if random.choice([1, 2]) == 1:
            answer += '{} '.format(random.choice(PREFIXES))

        answer += '{} i am {}.'.format(sender, core)
        answer.replace('?', '')

        if random.choice([1, 2]) == 1:
            answer += (' {}'.format(random.choice(SUFFIXES)))

        if random.choice([1, 3]) == 1:
            n = random.choice([1,2,3,4])
            emojis = ' '.join(random.sample(EMOJIS, n))
            answer += ' {}'.format(emojis)

        return answer

    @staticmethod
    def did_you(sender, message):
        _, question = message.split('did you')
        core, _ = question.split('?', 1)

        if core:
            core = make_subject_swaps(core)

        answer = ''

        if random.choice([1, 2]) == 1:
            answer += ('{} '.format(random.choice(PREFIXES)))

        answer += '{} i did {}.'.format(sender, core)
        message.replace('?', '')

        if random.choice([1, 2]) == 1:
            answer += ('  {}'.format(random.choice(SUFFIXES)))

        if random.choice([1, 3]) == 1:
            n = random.choice([1,2,3,4])
            emojis = ' '.join(random.sample(EMOJIS, n))
            answer += ' {}'.format(emojis)

        return answer

    @staticmethod
    def do_you(sender, message):
        _, question = message.split('do you')
        core, _ = question.split('?', 1)

        if core:
            core = make_subject_swaps(core)

        answer = ''

        if random.choice([1, 2]) == 1:
            answer += '{} '.format(random.choice(PREFIXES))

        answer += '{} i do {}.'.format(sender, core)
        answer.replace('?', '')

        if random.choice([1, 2]) == 1:
            answer += (' {}'.format(random.choice(SUFFIXES)))

        if random.choice([1, 3]) == 1:
            n = random.choice([1,2,3,4])
            emojis = ' '.join(random.sample(EMOJIS, n))
            answer += ' {}'.format(emojis)

        return answer

    @staticmethod
    def have_you(sender, message):
        _, question = message.split('have you')
        core, _ = question.split('?', 1)

        if core:
            if core.startswith(' ever'):
                core = core.replace(' ever', ' ')
            core = make_subject_swaps(core)

        answer = ''

        if random.choice([1, 2]) == 1:
            answer += '{} '.format(random.choice(PREFIXES))

        negate = 'not' if random.choice([1, 2]) == 1 else ''

        answer += '{} i have {}{}'.format(sender, negate, core)
        answer.replace('?', '')

        if random.choice([1, 2]) == 1:
            answer += (' {}'.format(random.choice(SUFFIXES)))

        if random.choice([1, 3]) == 1:
            n = random.choice([1,2,3,4])
            emojis = ' '.join(random.sample(EMOJIS, n))
            answer += ' {}'.format(emojis)

        return answer

    @staticmethod
    def will_you(sender, message):
        conjugations = {
            1: 'ill',
            2: 'i\'ll',
            3: 'i will',
            4: 'im gonna',
            5: 'i\'m going to',
        }

        _, question = message.split('will you')
        core, _ = question.split('?', 1)

        if core:
            if core.startswith(' ever'):
                core = core.replace(' ever', '') if random.choice([1, 2]) == 1 else ' never'
            if core.startswith(' please'):
                core = core.replace(' please', '')
            core = make_subject_swaps(core)

        answer = ''

        if random.choice([1, 2]) == 1:
            answer += '{} '.format(random.choice(PREFIXES))

        negate = 'not' if random.choice([1, 2]) == 1 else ''

        answer += '{} {} {}{}'.format(sender, random.choice(list(conjugations.values())), negate, core)
        answer.replace('?', '')

        if random.choice([1, 2]) == 1:
            answer += (' {}'.format(random.choice(SUFFIXES)))

        if random.choice([1, 3]) == 1:
            n = random.choice([1,2,3,4])
            emojis = ' '.join(random.sample(EMOJIS, n))
            answer += ' {}'.format(emojis)

        return answer

    @staticmethod
    def wanna(sender, message):
        _, question = message.split('wanna')
        core, _ = question.split('?', 1)

        if core:
            core = make_subject_swaps(core)

        answer = ''

        if random.choice([1, 2]) == 1:
            answer += '{} '.format(random.choice(PREFIXES))

        negate = 'not' if random.choice([1, 2]) == 1 else ''

        answer += '{} i wanna {}{}'.format(sender, negate, core)
        answer.replace('?', '')

        if random.choice([1, 2]) == 1:
            answer += (' {}'.format(random.choice(SUFFIXES)))

        if random.choice([1, 3]) == 1:
            n = random.choice([1,2,3,4])
            emojis = ' '.join(random.sample(EMOJIS, n))
            answer += ' {}'.format(emojis)

        return answer


def make_subject_swaps(core):
    return core.replace(' my ', ' your ').replace(' mine ', ' yours ').replace(' me ', ' you ').replace('bbot', '').replace(' i ', ' you ')