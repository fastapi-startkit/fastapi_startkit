import os
from fastapi_startkit_foundation import Application
from fastapi_startkit_foundation.providers import ConfigurationProvider

# Define your providers
# ConfigurationProvider is required to load your config files.
PROVIDERS = [
    ConfigurationProvider,
]

# Initialize the application
# base_path should point to the root where your 'config/' directory exists.
base_path = os.getcwd()
application = Application(base_path, PROVIDERS)
