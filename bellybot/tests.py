import json
import mock
import random

from django.urls import reverse
from django.test import TestCase

from bellybot.models import GroupMeBot, Answerer
from groupme_messages import MESSAGES

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

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_no_bot_response(self, mock_send):
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_not_called

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_speak(self, mock_send):
        GROUPME_CALLBACK["text"] = "bbot speak"
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_multiple_bbots(self, mock_send):
        GROUPME_CALLBACK["text"] = "bbot gif bbot"
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()


class TestBbotResponse(BellyBotTestCase):
    url = reverse('new_message')

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_get_bbot_from_message(self, mock_send):
        for member in self.members:
            GROUPME_CALLBACK["name"] = member
            GROUPME_CALLBACK["text"] = "i think bbot is really confused"
            self.client.post(self.url, GROUPME_CALLBACK)
            mock_send.assert_called_once()
            print(mock_send.call_args)
            mock_send.reset_mock()


class TestPlayerResponse(BellyBotTestCase):

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_get_player_from_message(self, mock_send):
        for player in self.players:
            GROUPME_CALLBACK["text"] = f"{player} is sucking wtf"
            self.client.post(self.url, GROUPME_CALLBACK)
            mock_send.assert_called_once()
            print(mock_send.call_args)
            mock_send.reset_mock()


class TestAnswerer(BellyBotTestCase):

    def test_why(self):
        questions = [
            'why dont you shit on lish bbot?',
            'bbot why is my team so shit?',
            'why didnt they go for 2 there bbot?',
            'bbot why arent i your fave bbr member?',
            'why do you love me bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer.why(sender, question)
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_are_you(self):
        questions = [
            'are you sure about that bbot?',
            'i don\'t know, are you gonna go?',
            'my thinking exactly. what are you gonna do about it?',
            'im not sure if im gonna go. are you?',
            'are you little botch who ran all the way home?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer.are_you(sender, question)
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_did_you(self):
        questions = [
            'did you really just say that bbot?',
            'i didnt know that, bbot did you know that?',
            'did you think we were done bbot??',
            'you didnt forget about me, did you?',
            'did you remember our little shotgun wager?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer.did_you(sender, question)
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
            response = Answerer.do_you(sender, question)
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
            response = Answerer.have_you(sender, question)
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))

    def test_will_you(self):
        questions = [
            'bbot will you remind me to do a shotgun later?',
            'sometimes im silly. will you take a second and be sharp bbot?',
            'what im wondering is will you ever make fun of me bbot?',
            'will you please shit on lish bbot?'
        ]
        for question in questions:
            sender = random.choice(self.members)
            response = Answerer.will_you(sender, question)
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
            response = Answerer.wanna(sender, question)
            assert isinstance(response, str)
            print('{}: {}'.format(sender, question))
            print('belly bot: {}'.format(response))
