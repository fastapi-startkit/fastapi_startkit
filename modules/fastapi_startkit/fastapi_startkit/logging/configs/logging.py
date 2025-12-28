from fastapi_startkit.environment.environment import env

DEFAULT = env('LOG_CHANNEL', 'single')

CHANNELS = {
    'timezone': env('LOG_TIMEZONE', 'UTC'),
    'single': {
        'driver': 'single',
        'level': 'debug',
        'path': 'storage/logs/single.log'
    },
    'stack': {
        'driver': 'stack',
        'channels': ['single', 'terminal']
    },
    'terminal': {
        'driver': 'terminal',
        'level': 'info'
    }
}
