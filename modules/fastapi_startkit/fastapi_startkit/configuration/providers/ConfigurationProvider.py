from ...providers import Provider

from ..Configuration import Configuration


class ConfigurationProvider(Provider):
    def register(self):
        config = Configuration(self.application)
        config.load()
        self.application.bind("config", config)

    def boot(self):
        pass
