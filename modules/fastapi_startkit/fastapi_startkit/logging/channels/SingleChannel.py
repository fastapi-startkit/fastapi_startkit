from ..factory import DriverFactory
from fastapi_startkit.facades import Config
from fastapi_startkit.utils.filesystem import make_directory
import os
import pendulum
from .BaseChannel import BaseChannel


class SingleChannel(BaseChannel):
    def __init__(self, driver=None, path=None):
        path = path or Config.get('logging.channels.single.path')
        make_directory(path)
        self.max_level = Config.get('logging.channels.single.level')
        self.driver = DriverFactory.make(driver or Config.get('logging.channels.single.driver'))(path=path, max_level=self.max_level)
