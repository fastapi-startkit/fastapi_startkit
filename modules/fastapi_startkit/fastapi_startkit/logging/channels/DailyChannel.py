from ..factory import DriverFactory
from fastapi_startkit.facades import Config
from fastapi_startkit.utils.filesystem import make_directory
import os
from .BaseChannel import BaseChannel

class DailyChannel(BaseChannel):

    def __init__(self, driver=None, path=None):
        path = path or Config.get('logging.channels.daily.path')
        path = os.path.join(path, self.get_time().to_date_string() + '.log')
        self.max_level = Config.get('logging.channels.daily.level')
        make_directory(path)
        self.driver = DriverFactory.make(driver or Config.get('logging.channels.daily.driver'))(path=path, max_level=self.max_level)

    def debug(self, message, *args, **kwargs):
        return self.driver.debug(message, *args, **kwargs)