import os
from fastapi_startkit.providers import Provider

from ..ChannelFactory import ChannelFactory
from ..Logger import Logger
from ..factory import DriverFactory
from ..listeners import LoggerExceptionListener
from ..managers import LoggingManager


class LoggingProvider(Provider):
    def register(self):
        self.merge_config_from(self.config, 'logging')
        source = os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs/logging.py"))
        self.merge_config_from(source, 'logging')

        self.application.bind('LogChannelFactory', ChannelFactory)
        self.application.bind('LogDriverFactory', DriverFactory)
        self.application.bind('LoggingManager', LoggingManager(ChannelFactory, DriverFactory))
        self.application.simple(LoggerExceptionListener)

    def boot(self):
        source = os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs/logging.py"))
        self.publishes({
            source: 'config/logging.py'
        })
        config = self.application.make('config')
        if not config.get('logging.default'):
            return
        logger = self.application.make('LoggingManager')
        channel = logger.channel(config.get('logging.default'))

        self.application.bind('logger', channel)
        self.application.swap(Logger, channel)

        self.application.make('logger').info(self.config)
