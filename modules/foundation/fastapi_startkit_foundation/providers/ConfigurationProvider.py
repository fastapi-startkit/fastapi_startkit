from .Provider import Provider
from ..configuration import Configuration
import os

class ConfigurationProvider(Provider):
    def register(self):
        self.application.bind('config.location', os.path.join(self.application.base_path, "config"))
        configuration = Configuration(self.application)
        configuration.load()
        self.application.bind("config", configuration)

    def boot(self):
        pass
