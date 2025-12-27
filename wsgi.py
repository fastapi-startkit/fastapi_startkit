import os
from fastapi_startkit import Application
from fastapi_startkit.configuration.providers import ConfigurationProvider
from fastapi_startkit.logging.providers import LoggingProvider

# Define your providers
PROVIDERS = [
    ConfigurationProvider,
    LoggingProvider
]

# Initialize the application
base_path = os.getcwd()
application = Application(base_path, PROVIDERS)
