class LoggingManager:

    # config = 'LoggingConfig'
    # driver_prefix = 'Logging'

    def __init__(self, channel_factory=None, driver_factory=None):
        self.channel_factory = channel_factory
        self.driver_factory = driver_factory

    def channel(self, channel):
        return self.channel_factory.make(channel)()