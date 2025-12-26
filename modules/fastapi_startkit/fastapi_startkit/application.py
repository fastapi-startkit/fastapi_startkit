from fastapi import FastAPI

from .container import Container
from .environment.environment import LoadEnvironment


class Application(Container):
    def __init__(self, base_path: str = None, providers=None):
        self.base_path: str = base_path
        self.providers = providers if providers else []

        self.load_environment()
        self.register_providers()

        self.fastapi = FastAPI()
        self.load_providers()

    def register_providers(self):
        for provider_class in self.providers:
            provider = provider_class(self)
            provider.register()
        return self

    def load_providers(self):
        for provider in self.providers:
            self.resolve(provider.boot)
        return self

    def use_fastapi(self, fastapi: FastAPI):
        self.fastapi = fastapi
        return self

    def get(self, path: str):
        return self.fastapi.get(path)

    def __call__(self):
        return self.fastapi

    def load_environment(self):
        LoadEnvironment(base_path=self.base_path)
