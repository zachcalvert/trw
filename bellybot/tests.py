import json
import mock

from django.urls import reverse
from django.test import TestCase


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

    def test_get_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_no_bot_response(self, mock_send):
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_not_called

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_commercial_in_message(self, mock_send):
        GROUPME_CALLBACK["text"] = "Hello commercial"
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once_with("We don't do commercials in the pit!", None)

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_shotgun_in_message(self, mock_send):
        GROUPME_CALLBACK["text"] = "Hello shotgun"
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_speak(self, mock_send):
        GROUPME_CALLBACK["text"] = "bbot speak"
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_questions(self, mock_send):
        GROUPME_CALLBACK["text"] = "bbot where do the saints play"
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_questions(self, mock_send):
        GROUPME_CALLBACK["text"] = "bbot what is the meaning of life"
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_questions(self, mock_send):
        GROUPME_CALLBACK["text"] = "bbot what day of the week is the super bowl this year"
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()

    @mock.patch('bellybot.models.GroupMeBot.send_message')
    def test_multiple_bbots(self, mock_send):
        GROUPME_CALLBACK["text"] = "bbot gif bbot"
        self.client.post(self.url, GROUPME_CALLBACK)
        mock_send.assert_called_once()

    # def test_real_message(self):
    #     GROUPME_CALLBACK["text"] = "whos doing an ice?"
    #     self.client.post(self.url, GROUPME_CALLBACK)
    #
    # def test_real_image(self):
    #     GROUPME_CALLBACK["text"] = "bb image aww yeaa"
    #     self.client.post(self.url, GROUPME_CALLBACK)
    #
    # def test_real_gif(self):
    #     GROUPME_CALLBACK["text"] = "bb gif yaw!"
    #     self.client.post(self.url, GROUPME_CALLBACK)
    #
    # def test_speak(self):
    #     GROUPME_CALLBACK["text"] = "BB SPeaK"
    #     self.client.post(self.url, GROUPME_CALLBACK)
    #
    # def test_unknown(self):
    #     GROUPME_CALLBACK["text"] = "BB what are you doing"
    #     self.client.post(self.url, GROUPME_CALLBACK)
