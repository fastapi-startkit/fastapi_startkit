""" Logging Settings """

import os
from fastapi_startkit.environment.environment import env

"""Default Channel
"""

DEFAULT=env('LOG_CHANNEL', 'single')

"""Channels
"""
CHANNELS = {
    'timezone': env('LOG_TIMEZONE', 'UTC'),
    'single': {
        'driver': 'single',
        'level': 'debug',
        'path': 'storage/logs/single.log'
    },
    'stack': {
        'driver': 'stack',
        'channels': ['single', 'daily', 'slack', 'terminal']
    },
    'daily': {
        'driver': 'daily',
        'level': 'debug',
        'path': 'storage/logs'
    },
    'terminal': {
        'driver': 'terminal',
        'level': 'info',
    },
    'slack': {
        'driver': 'slack',
        'channel': '#bot',
        'emoji': ':warning:',
        'username': 'Logging Bot',
        'token': env('SLACK_TOKEN', None),
        'level': 'debug'
    },
    'syslog': {
        'driver': 'syslog',
        'path': '/var/run/syslog',
        'level': 'debug'
    }
}