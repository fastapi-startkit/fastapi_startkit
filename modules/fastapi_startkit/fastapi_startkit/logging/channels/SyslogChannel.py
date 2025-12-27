from ..factory import DriverFactory
from fastapi_startkit.facades import Config
from fastapi_startkit.utils.filesystem import make_directory
import os
import pendulum
from .BaseChannel import BaseChannel

class SyslogChannel(BaseChannel):

    def __init__(self, driver=None, path=None):
        path = path or Config.get('logging.channels.syslog.path')
        make_directory(path)
        self.max_level = Config.get('logging.channels.syslog.level')
        self.driver = DriverFactory.make(driver or Config.get('logging.channels.syslog.driver'))(path=path, max_level=self.max_level)
