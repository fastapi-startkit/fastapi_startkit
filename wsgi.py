import os
from fastapi_startkit import Application
from fastapi_startkit.logging.providers import LoggingProvider

# Define your providers
PROVIDERS = [
    (LoggingProvider, {
        'default': 'single',
        'channels': {
            'single': {
                'driver': 'single',
                'level': 'debug',
                'path': 'storage/logs/single.log'
            },
        }
    })
]

# Initialize the application
base_path = os.getcwd()
application = Application(base_path, PROVIDERS)
