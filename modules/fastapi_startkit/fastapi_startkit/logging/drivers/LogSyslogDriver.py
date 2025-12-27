from .BaseDriver import BaseDriver
import logging
import logging.handlers

class LogSyslogDriver(BaseDriver):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger('root')
        path = kwargs.get('path')
        
        handler = logging.handlers.SysLogHandler(address = path)

        formatter = logging.Formatter('{} - %(levelname)s - %(message)s'.format(self.get_time().to_datetime_string()))
        handler.setFormatter(formatter)

        self.log.addHandler(handler)

    def emergency(self, message):
        self.log.setLevel(logging.CRITICAL)
        return self.log.critical(message)

    def alert(self, message):
        self.log.setLevel(logging.CRITICAL)
        return self.log.critical(message)

    def critical(self, message):
        self.log.setLevel(logging.CRITICAL)
        return self.log.critical(message)

    def error(self, message):
        self.log.setLevel(logging.ERROR)
        return self.log.error(message)

    def warning(self, message):
        self.log.setLevel(logging.WARNING)
        return self.log.warning(message)

    def notice(self, message):
        self.log.setLevel(logging.NOTICE)
        return self.log.info(message)

    def info(self, message):
        self.log.setLevel(logging.INFO)
        return self.log.info(message)

    def debug(self, message):
        self.log.setLevel(logging.DEBUG)
        return self.log.debug(message)