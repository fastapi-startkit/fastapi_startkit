import os
from .BaseDriver import BaseDriver
import requests

class LogSlackDriver(BaseDriver):

    def __init__(self, *args, **kwargs):
        self.slack_url = 'https://slack.com/api/chat.postMessage'
        self.token = kwargs.get('token')
        self.channel = kwargs.get('channel')
        self.emoji = kwargs.get('emoji', ':warning:')
        self.username = kwargs.get('username')

    def emergency(self, message, *args, **kwargs):
        self.send(
            self.get_format(message, 'EMERGENCY')
        )

    def alert(self, message, *args, **kwargs):
        self.send(
            self.get_format(message, 'ALERT')
        )

    def critical(self, message, *args, **kwargs):
        self.send(
            self.get_format(message, 'CRITICAL')
        )

    def error(self, message, *args, **kwargs):
        self.send(
            self.get_format(message, 'ERROR')
        )

    def warning(self, message, *args, **kwargs):
        self.send(
            self.get_format(message, 'WARNING')
        )

    def notice(self, message, *args, **kwargs):
        self.send(
            self.get_format(message, 'NOTICE')
        )

    def info(self, message, *args, **kwargs):
        self.send(
            self.get_format(message, 'INFO')
        )

    def debug(self, message, *args, **kwargs):
        self.send(
            self.get_format(message, 'DEBUG')
        )

    def get_format(self, message, level):
        return "{time} - {level} - {message}".format(
            time=self.get_time().to_datetime_string(),
            message=message,
            level=level
        )

    def send(self, message):
        requests.post(self.slack_url, {
            'token': self.token,
            'channel': self.find_channel(self.channel),
            'text': message,
            'username': self.username,
            'icon_emoji': self.emoji,
            'as_user': False,
            'reply_broadcast': True,
            'unfurl_links': True,
            'unfurl_media': True,
        })

    def find_channel(self, name):
        """Calls the Slack API to find the channel name. 
        This is so we do not have to specify the channel ID's. Slack requires channel ID's
        to be used.
        Arguments:
            name {string} -- The channel name to find.
        Raises:
            SlackChannelNotFound -- Thrown if the channel name is not found.
        Returns:
            self
        """
        response = requests.post('https://slack.com/api/channels.list', {
            'token': self.token
        })

        for channel in response.json()['channels']:
            if channel['name'] == name.split('#')[1]:
                return channel['id']

        raise SlackChannelNotFound(
            'Could not find the {} channel'.format(name))
