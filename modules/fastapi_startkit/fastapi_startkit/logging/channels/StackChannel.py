from ..factory import DriverFactory
from fastapi_startkit.facades import Config
import os
import pendulum
from .MultiBaseChannel import MultiBaseChannel

class StackChannel(MultiBaseChannel):

    def __init__(self, channels=[]):
        channels = channels or Config.get('logging.channels.stack.channels')
        from ..ChannelFactory import ChannelFactory
        self.channels = []
        for channel in channels:
            channel = ChannelFactory.make(channel)()
            self.channels.append(channel)
    
    def debug(self, message, *args, **kwargs):
        for channel in self.channels:
            if not channel.driver.should_run('debug', channel.max_level):
                continue
            
            channel.driver.debug(message, *args, **kwargs)
            
    def notice(self, message, *args, **kwargs):
        for channel in self.channels:
            if not channel.driver.should_run('notice', channel.max_level):
                continue
            
            channel.driver.notice(message, *args, **kwargs)

