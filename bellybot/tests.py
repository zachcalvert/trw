import json
import mock
import random

from django.urls import reverse
from django.test import TestCase

from bellybot.models import GroupMeBot
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


# class BellyBotTestCase(TestCase):
#
#     url = reverse('new_message')
#
#     def test_get_not_allowed(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 405)
#
#     @mock.patch('bellybot.models.GroupMeBot.send_message')
#     def test_no_bot_response(self, mock_send):
#         self.client.post(self.url, GROUPME_CALLBACK)
#         mock_send.assert_not_called
#
#     @mock.patch('bellybot.models.GroupMeBot.send_message')
#     def test_speak(self, mock_send):
#         GROUPME_CALLBACK["text"] = "bbot speak"
#         self.client.post(self.url, GROUPME_CALLBACK)
#         mock_send.assert_called_once()

    # @mock.patch('bellybot.models.GroupMeBot.send_message')
    # def test_where(self, mock_send):
    #     GROUPME_CALLBACK["text"] = "bbot where do the saints play"
    #     self.client.post(self.url, GROUPME_CALLBACK)
    #     mock_send.assert_called_once()
    #
    # @mock.patch('bellybot.models.GroupMeBot.send_message')
    # def test_what(self, mock_send):
    #     GROUPME_CALLBACK["text"] = "bbot what day of the week is the super bowl this year"
    #     self.client.post(self.url, GROUPME_CALLBACK)
    #     mock_send.assert_called_once()

#     @mock.patch('bellybot.models.GroupMeBot.send_message')
#     def test_multiple_bbots(self, mock_send):
#         GROUPME_CALLBACK["text"] = "bbot gif bbot"
#         self.client.post(self.url, GROUPME_CALLBACK)
#         mock_send.assert_called_once()
#

class TestBBRResponse(TestCase):
    url = reverse('new_message')

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_get_bbot_from_message(self, mock_send):
        GROUPME_CALLBACK["text"] = "i think bbot is really confused"
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()
        print(mock_send.call_args)


class TestPlayerResponse(TestCase):

    url = reverse('new_message')

    players = ['Travis Kelce', 'Dalvin Cook', 'Deshaun Watson', 'Brandin Cooks', 'Chase Claypool']
    members = ['shane', 'trav', 'bk', 'rene', 'lish']

    def test_player_response(self):
        for member in self.members:
            print(GroupMeBot().generate_bbr_response(member))
            for player in self.players:
                print(GroupMeBot().generate_player_response(member, player))
#
#     @mock.patch('bellybot.models.GroupMeBot.send_message')
#     def test_get_player_from_message(self, mock_send):
#         GROUPME_CALLBACK["text"] = "jackson is sucking wtf"
#         self.client.post(self.url, GROUPME_CALLBACK)
#         mock_send.assert_called_once()
#         print(mock_send.call_args)


# class TestMarkovRespond(TestCase):
#
#     def test_random_responses(self):
#         for i in range(1000):
#             message = random.choice(MESSAGES).lower()
#             print(GroupMeBot().markov_respond('zach', message))

    # def test_brees(self):
    #     print(GroupMeBot().smart_respond('zach', 'Last year Drew Brees won the super bowl'))
    #
    # def test_question(self):
    #     print(GroupMeBot().smart_respond('zach', 'What do you think about that bbot'))
    #
    # def test_shane(self):
    #     print(GroupMeBot().smart_respond('zach', 'Shane is stoked about the win'))
    #
    # def test_waiver(self):
    #     print(GroupMeBot().smart_respond('zach', 'My waiver pickup this week is nasty'))





# class TestRealResponse(TestCase):
#
#     url = reverse('new_message')
#
#     def test_real_image(self):
#         GROUPME_CALLBACK["text"] = "bb image aww yeaa"
#         self.client.post(self.url, GROUPME_CALLBACK)
#
#     def test_real_gif(self):
#         GROUPME_CALLBACK["text"] = "bb gif yaw!"
#         self.client.post(self.url, GROUPME_CALLBACK)
#
#     def test_speak(self):
#         GROUPME_CALLBACK["text"] = "BB SPeaK"
#         self.client.post(self.url, GROUPME_CALLBACK)
#
#     def test_bbot_mentioned(self):
#         GROUPME_CALLBACK["text"] = "Lol wtf is going on with BBot "
#         self.client.post(self.url, GROUPME_CALLBACK)
#
#     def test_player_mentioned(self):
#         GROUPME_CALLBACK["text"] = "Lol wtf is going on with elliott "
#         self.client.post(self.url, GROUPME_CALLBACK)
#
#     def test_unknown(self):
#         GROUPME_CALLBACK["text"] = "BB what are you doing"
#         self.client.post(self.url, GROUPME_CALLBACK)