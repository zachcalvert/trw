import mock
import random

from django.urls import reverse
from django.test import TestCase

from bellybot.answerer import Answerer

GROUPME_CALLBACK = {
  "attachments": [],
  "avatar_url": "https://i.groupme.com/123456789",
  "created_at": 1302623328,
  "group_id": "1234567890",
  "id": "1234567890",
  "name": "Lick Manheole",
  "sender_id": "12345",
  "sender_type": "user",
  "source_guid": "GUID",
  "system": False,
  "text": "Hello world",
  "user_id": "1234567890"
}

headers = {'Content-Type': 'application/json'}


class BellyBotTestCase(TestCase):

    url = reverse('new_message')
    players = ['Travis Kelce', 'Dalvin Cook', 'Deshaun Watson', 'Brandin Cooks', 'Chase Claypool']
    members = ['shane', 'trav', 'bk', 'rene', 'lish', 'walsh', 'bk', 'vino', 'commish']

    def test_get_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    @mock.patch('bellybot.bbot.BellyBot.send_message')
    def test_no_bot_response(self, mock_send):
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_not_called

    @mock.patch('bellybot.bbot.BellyBot.send_message')
    def test_multiple_bbots(self, mock_send):
        GROUPME_CALLBACK["text"] = "bbot gif bbot"
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()


class TestBbotResponse(BellyBotTestCase):
    url = reverse('new_message')

    @mock.patch('bellybot.bbot.BellyBot.send_message')
    def test_get_bbot_from_message(self, mock_send):
        for member in self.members:
            GROUPME_CALLBACK["name"] = member
            GROUPME_CALLBACK["text"] = "i think bbot is really confused"
            self.client.post(self.url, GROUPME_CALLBACK)
            mock_send.assert_called_once()
            print(mock_send.call_args)
            mock_send.reset_mock()


class TestQuestionResponse(BellyBotTestCase):

    questions_that_get_responses = [
        'why dont you shit on lish bbot?',
        'when am i gonna win a damn game bbot?',
        'bbot how are you this morning?',
        'who gave you the right bbot?',
        'where are you from bbot?',
        'are you sure about that bbot?',
        'did you remember our little shotgun wager bbot?',
        'wanna blast cigs in the parking lot bbot?',
        'do you think i should start deshaun bbot?',
        'bbot will you remind me to do a shotgun later?',
        'have you eaten your vegetables today bbot?',
        'bbot comment on deshaun watson please'
    ]

    questions_that_dont_get_responses = [
        'why dont you shit on lish?',
        'when am i gonna win a damn game?',
        'how are you this morning?',
        'who gave you the right?',
        'where are you from?',
        'what do you think about deshaun watson?'
    ]

    @mock.patch('bellybot.bbot.BellyBot.send_message')
    def test_question_response(self, mock_send):
        for question in self.questions_that_get_responses:
            GROUPME_CALLBACK["text"] = question
            self.client.post(self.url, GROUPME_CALLBACK)
            mock_send.assert_called_once()
            print(mock_send.call_args)
            mock_send.reset_mock()

    @mock.patch('bellybot.bbot.BellyBot.send_message')
    def test_question_no_response(self, mock_send):
        for question in self.questions_that_dont_get_responses:
            GROUPME_CALLBACK["text"] = question
            self.client.post(self.url, GROUPME_CALLBACK)
            mock_send.assert_not_called
            mock_send.reset_mock()


class TestAnswerer(TestCase):

    players = ['Travis Kelce', 'Dalvin Cook', 'Deshaun Watson', 'Brandin Cooks', 'Chase Claypool']
    members = ['shane', 'trav', 'bk', 'rene', 'lish', 'walsh', 'bk', 'vino', 'commish']

    def test_what(self):
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
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_why(self):
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
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_when(self):
        questions = [
            'when am i gonna win a damn game bbot?',
            'bbot when will you respect me?',
            'when is a good time to talk bbot?',
            'bbot when do you go back to school?',
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_how(self):
        questions = [
            'how are you so smart and so dumb bbot?',
            'bbot how are you this morning?',
            'how is everything going bbot?',
            'bbot how do you know these things?',
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_who(self):
        questions = [
            'who gave you the right bbot?',
            'bbot who is your favorite chiefs player?',
            'who hurt you bbot?',
            'bbot who are you in love with?',
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_where(self):
        questions = [
            'where are you from bbot?',
            'bbot where are you looking forward to going next?',
            'where does this come from bbot?',
            'bbot where were you anyway?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_are_you(self):
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
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_did_you(self):
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
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_do_you(self):
        questions = [
            'do you think i should start deshaun bbot?',
            'i know its true bbot. do you know that though?',
            'bbot do you wanna get in on a lil shotgun bet?',
            'im thinking about it, do you think it could work bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_have_you(self):
        questions = [
            'have you eaten your vegetables today bbot?',
            'i just set my lineup bbot. have you?',
            'have you ever been to Germany bbot? Ive never been',
            'have you forgotten where you come from bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_will_you(self):
        questions = [
            'bbot will you remind me to do a shotgun later?',
            'sometimes im silly. will you take a second and be sharp bbot?',
            'im wondering, will you ever make fun of me bbot?',
            'will you please shit on lish bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_wanna(self):
        questions = [
            'bbot wanna do a strikeout later?',
            'wanna go ahead and look that up for us bbot?',
            'bbot any chance you wanna think some more about that?',
            'wanna blast cigs in the parking lot bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))


class TestNewNickname(TestCase):

    members = ['shane', 'trav', 'bk', 'rene', 'lish', 'walsh', 'bk', 'vino', 'commish']

    def test_new_nickname(self):
        questions = [
            'bbot can I get a new nickname?',
            'bbot how about another nickname?',
            'can i get another nickname bbot',
            'sure would love a new nickname bbot',
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer(sender, question).answer()
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))


class TestFavoriteTeam(TestCase):

    def test_new_nickname(self):
        messages = [
            'bbot who is your favorite team?',
            'bbot do you like the lions?',
            'woah the lions won',
        ]

        @mock.patch('bellybot.bbot.BellyBot.send_message')
        def test_question_response(self, mock_send):
            for message in messages:
                GROUPME_CALLBACK["text"] = message
                self.client.post(self.url, GROUPME_CALLBACK)
                mock_send.assert_called_once()
                assert 'GO LIONS!' in mock_send.call_args
                print(mock_send.call_args)
                mock_send.reset_mock()


class TestJoke(BellyBotTestCase):

    messages = [
        'bbot joke hopkins',
        'tell me a joke bbot',
        'would love another joke bbot'
    ]

    def test_question_response(self):
        for message in self.messages:
            sender = random.choice(self.members)
            response = Answerer(sender, message, player='deshaun watson').answer()
            assert isinstance(response, str)
            print('{}: {}'.format(sender, message))
            print('belly bot: {}'.format(response))

    @mock.patch('bellybot.bbot.BellyBot.send_message')
    def test_question_response(self, mock_send):
        for question in self.messages:
            GROUPME_CALLBACK["text"] = question
            self.client.post(self.url, GROUPME_CALLBACK)
            mock_send.assert_called_once()
            print(mock_send.call_args)
            mock_send.reset_mock()


class TestExcuses(TestCase):

    member = 'zach'
    message = 'what do you think about that bbot?'

    def test_question_response(self):
        for i in range(50):
            print(Answerer(self.member,self. message).give_update())
