import mock
import random

from django.urls import reverse
from django.test import TestCase

from bellybot.answerer import Answerer
from bellybot.bbot import USER_MAP

GROUPME_CALLBACK = {
  "attachments": [],
  "avatar_url": "https://i.groupme.com/123456789",
  "created_at": 1302623328,
  "group_id": "1234567890",
  "id": "1234567890",
  "name": "Lick Manheole",
  "sender_id": "30837252",
  "sender_type": "user",
  "source_guid": "GUID",
  "system": False,
  "text": "Hello world",
  "user_id": random.choice(list(USER_MAP.keys()))
}

headers = {'Content-Type': 'application/json'}


class BellyBotTestCase(TestCase):

    url = reverse('new_message')
    players = ['Travis Kelce', 'Dalvin Cook', 'Deshaun Watson', 'Brandin Cooks', 'Chase Claypool']
    members = ['shane', 'trav', 'bk', 'rene', 'lish', 'walsh', 'bk', 'vino', 'commish']

    def test_get_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    @mock.patch('bellybot.Responder.send_message')
    def test_no_bot_response(self, mock_send):
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_not_called


class TestBbotResponse(BellyBotTestCase):
    url = reverse('new_message')

    @mock.patch('bellybot.Responder.send_message')
    def test_get_bbot_from_message(self, mock_send):
        for member in self.members:
            GROUPME_CALLBACK["name"] = member
            GROUPME_CALLBACK["user_id"] = random.choice(list(USER_MAP.keys()))
            GROUPME_CALLBACK["text"] = "i think bbot is really confused"
            self.client.post(self.url, GROUPME_CALLBACK)
            mock_send.assert_called_once()
            print(mock_send.call_args)
            mock_send.reset_mock()


class TestQuestionsIgnored(BellyBotTestCase):

    questions_that_dont_get_responses = [
        'why dont you shit on lish?',
        'when am i gonna win a damn game?',
        'how are you this morning?',
        'who gave you the right?',
        'where are you from?',
        'what do you think about deshaun watson?'
    ]

    @mock.patch('bellybot.Responder.send_message')
    def test_question_no_response(self, mock_send):
        for question in self.questions_that_dont_get_responses:
            GROUPME_CALLBACK["text"] = question
            self.client.post(self.url, GROUPME_CALLBACK)
            mock_send.assert_not_called
            mock_send.reset_mock()


class TestAnswerer(BellyBotTestCase):

    players = ['Travis Kelce', 'Dalvin Cook', 'Deshaun Watson', 'Brandin Cooks', 'Chase Claypool']
    members = ['shane', 'trav', 'bk', 'rene', 'lish', 'walsh', 'bk', 'vino', 'commish']

    @mock.patch('bellybot.Responder.send_message')
    def test_what(self, mock_send):
        questions = [
            'bbot whats the plan tonight?',
            'what do you think about Watson bbot?',
            'what is your purpose bbot?',
            'bbot what can I do to help?',
            'what is the point of all this bbot?',
            'what do you want from life bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_why(self, mock_send):
        questions = [
            'bbot why dont you shit on lish?',
            'bbot why is my team so shit?',
            'why didnt they go for 2 there bbot?',
            'bbot why arent i your fave bbr member?',
            'why do you love me bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_when(self, mock_send):
        questions = [
            'when am i gonna win a damn game bbot?',
            'bbot when will you respect me?',
            'when is a good time to talk bbot?',
            'bbot when do you go back to school?',
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_how(self, mock_send):
        questions = [
            'how are you so smart and so dumb bbot?',
            'bbot how are you this morning?',
            'how is everything going bbot?',
            'bbot how do you know these things?',
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_who(self, mock_send):
        questions = [
            'who gave you the right bbot?',
            'bbot who is your favorite chiefs player?',
            'who hurt you bbot?',
            'bbot who are you in love with?',
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_where(self, mock_send):
        questions = [
            'where are you from bbot?',
            'bbot where are you looking forward to going next?',
            'where does this come from bbot?',
            'bbot where were you anyway?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_are_you(self, mock_send):
        questions = [
            'are you sure about that bbot?',
            'i don\'t know, are you gonna go?',
            'my thinking exactly. what are you gonna do about it?',
            'im not sure if im gonna go. are you?',
            'are you a little botch who ran all the way home?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_did_you(self, mock_send):
        questions = [
            'did you really just say that bbot?',
            'i didnt know that, bbot did you know that?',
            'did you think we were done bbot??',
            'you didnt forget about me, did you?',
            'did you remember our little shotgun wager bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_do_you(self, mock_send):
        questions = [
            'do you think i should start deshaun bbot?',
            'i know its true bbot. do you know that though?',
            'bbot do you wanna get in on a lil shotgun bet?',
            'im thinking about it, do you think it could work bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_have_you(self, mock_send):
        questions = [
            'have you eaten your vegetables today bbot?',
            'i just set my lineup bbot. have you?',
            'have you ever been to Germany bbot? Ive never been',
            'have you forgotten where you come from bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_will_you(self, mock_send):
        questions = [
            'bbot will you remind me to do a shotgun later?',
            'sometimes im silly. will you take a second and be sharp bbot?',
            'im wondering, will you ever make fun of me bbot?',
            'will you please shit on lish bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_wanna(self, mock_send):
        questions = [
            'bbot wanna do a strikeout later?',
            'wanna go ahead and look that up for us bbot?',
            'bbot any chance you wanna think some more about that?',
            'wanna blast cigs in the parking lot bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_right_bbot(self, mock_send):
        questions = [
            'thats a good one, right bbot?',
            'right bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_chyaa(self, mock_send):
        questions = [
            'can i get a chyaaaaa bbot?',
            'bbot i love it chyaa'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.Responder.send_message')
    def test_eyaww(self, mock_send):
        message = 'bbot eyaww'

        GROUPME_CALLBACK["text"] = message
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()
        print(mock_send.call_args)
        mock_send.reset_mock()

    @mock.patch('bellybot.Responder.send_message')
    def test_good_morning(self, mock_send):
        message = 'good morning bbot'
        GROUPME_CALLBACK["user_id"] = random.choice(list(USER_MAP.keys()))
        GROUPME_CALLBACK["text"] = message
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()
        print(mock_send.call_args)
        mock_send.reset_mock()


class TestNewNickname(TestCase):

    members = ['shane', 'trav', 'bk', 'rene', 'lish', 'walsh', 'bk', 'vino', 'commish']

    @mock.patch('bellybot.Responder.send_message')
    def test_new_nickname(self, mock_send):
        questions = [
            'bbot can I get a new nickname?',
            'bbot how about another nickname?',
            'can i get another nickname bbot',
            'sure would love a new nickname bbot',
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))


class TestAllCapsForLish(BellyBotTestCase):

    messages = [
        'bbot who is your favorite team?',
        'whatup bbot',
    ]

    @mock.patch('bellybot.Responder.send_message')
    def test_lish_responses(self, mock_send):
        for message in self.messages:
            GROUPME_CALLBACK["text"] = message
            GROUPME_CALLBACK["user_id"] = '4689709'
            self.client.post(self.url, GROUPME_CALLBACK)
            mock_send.assert_called_once()
            print(mock_send.call_args)
            mock_send.reset_mock()


class TestFavoriteTeam(BellyBotTestCase):

    messages = [
        'bbot who is your favorite team?',
        'bbot gif alcoholic',
    ]

    @mock.patch('bellybot.Responder.send_message')
    def test_lions_responses(self, mock_send):
        for message in self.messages:
            GROUPME_CALLBACK["text"] = message
            self.client.post(self.url, GROUPME_CALLBACK)
            mock_send.assert_called_once()
            print(mock_send.call_args)
            mock_send.reset_mock()


class TestEspnWrapper(TestCase):

    url = reverse('new_message')

    # @mock.patch('bellybot.Responder.send_message')
    # def test_trophies(self, mock_send):
    #     message = 'bbot week 7 trophies'
    #
    #     GROUPME_CALLBACK["text"] = message
    #     self.client.post(self.url, GROUPME_CALLBACK)
    #     mock_send.assert_called_once()
    #     print(mock_send.call_args)
    #     mock_send.reset_mock()
    #
    # @mock.patch('bellybot.Responder.send_message')
    # def test_matchups(self, mock_send):
    #     message = 'bbot week 8 matchups'
    #
    #     GROUPME_CALLBACK["text"] = message
    #     self.client.post(self.url, GROUPME_CALLBACK)
    #     mock_send.assert_called_once()
    #     print(mock_send.call_args)
    #     mock_send.reset_mock()

    @mock.patch('bellybot.Responder.send_message')
    def test_average_scores(self, mock_send):
        message = 'bbot average points scored'

        GROUPME_CALLBACK["text"] = message
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()
        print(mock_send.call_args)
        mock_send.reset_mock()

    @mock.patch('bellybot.Responder.send_message')
    def test_average_points_against(self, mock_send):
        message = 'bbot average points against'

        GROUPME_CALLBACK["text"] = message
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()
        print(mock_send.call_args)
        mock_send.reset_mock()

    @mock.patch('bellybot.Responder.send_message')
    def test_help_message(self, mock_send):
        message = 'bbot help'

        GROUPME_CALLBACK["text"] = message
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()
        print(mock_send.call_args)
        mock_send.reset_mock()

    # @mock.patch('bellybot.Responder.send_message')
    # def test_final_standings(self, mock_send):
    #     message = 'bbot final standings'
    #
    #     GROUPME_CALLBACK["text"] = message
    #     self.client.post(self.url, GROUPME_CALLBACK)
    #     mock_send.assert_called_once()
    #     print(mock_send.call_args)
    #     mock_send.reset_mock()

    @mock.patch('bellybot.Responder.send_message')
    def test_trade(self, mock_send):
        message = 'bbot trade'

        for i in range(10):
            GROUPME_CALLBACK["text"] = message
            self.client.post(self.url, GROUPME_CALLBACK)
            mock_send.assert_called_once()
            print(mock_send.call_args)
            mock_send.reset_mock()
