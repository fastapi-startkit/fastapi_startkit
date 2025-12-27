
from ..factory import DriverFactory
from fastapi_startkit.facades import Config
import os
import pendulum
from .BaseChannel import BaseChannel

class SlackChannel(BaseChannel):

    def __init__(self, driver=None, path=None):
        token = Config.get('logging.channels.slack.token')
        channel = Config.get('logging.channels.slack.channel')
        emoji = Config.get('logging.channels.slack.emoji')
        username = Config.get('logging.channels.slack.username')
        self.max_level = Config.get('logging.channels.slack.level')
        self.driver = DriverFactory.make(driver or Config.get('logging.channels.slack.driver'))(emoji=emoji, username=username, token=token, channel=channel)

    def debug(self, message, *args, **kwargs):
        return self.driver.debug(message, *args, **kwargs)