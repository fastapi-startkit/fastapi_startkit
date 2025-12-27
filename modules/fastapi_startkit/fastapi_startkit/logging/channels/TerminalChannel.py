import os

import pendulum
from fastapi_startkit.facades import Config

from ..factory import DriverFactory
from ..channels.BaseChannel import BaseChannel


class TerminalChannel(BaseChannel):

    def __init__(self, driver=None, path=None):
        self.max_level = Config.get('logging.channels.terminal.level', 'debug')
        self.driver = DriverFactory.make(driver or Config.get('logging.channels.terminal.driver'))(path=path, max_level=self.max_level)
