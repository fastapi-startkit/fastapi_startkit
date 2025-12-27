# from logging import Logger
import os

from fastapi_startkit.facades import Config
from fastapi_startkit.utils.console import HasColoredOutput

from .BaseDriver import BaseDriver


class LogTerminalDriver(BaseDriver, HasColoredOutput):

    def __init__(self, *args, **kwargs):
        pass

    def emergency(self, message):
        super().warning(
            self.get_format(message, 'EMERGENCY')
        )

    def alert(self, message):
        super().warning(
            self.get_format(message, 'ALERT')
        )

    def critical(self, message):
        super().warning(
            self.get_format(message, 'CRITICAL')
        )

    def error(self, message):
        super().warning(
            self.get_format(message, 'ERROR')
        )

    def warning(self, message):
        super().warning(
            self.get_format(message, 'WARNING')
        )

    def notice(self, message):
        super().warning(
            self.get_format(message, 'NOTICE')
        )

    def info(self, message):
        super().warning(
            self.get_format(message, 'INFO')
        )

    def debug(self, message):
        super().warning(
            self.get_format(message, 'DEBUG')
        )

    def get_format(self, message, level):
        return '{time} - {level} - {message}'.format(
                time=self.get_time().to_datetime_string(),
                level=level,
                message=message
            )