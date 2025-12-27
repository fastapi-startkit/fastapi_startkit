import pendulum
from fastapi_startkit.facades import Config

class BaseChannel:

    def get_time(self):
        
        return pendulum.now().in_tz(Config.get('logging.channels.timezone', 'UTC'))

    def emergency(self, message, *args, **kwargs):
        if not self.driver.should_run('emergency', self.max_level):
            return

        return self.driver.emergency(message, *args, **kwargs)

    def alert(self, message, *args, **kwargs):
        if not self.driver.should_run('alert', self.max_level):
            return

        return self.driver.alert(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        if not self.driver.should_run('critical', self.max_level):
            return

        return self.driver.critical(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        if not self.driver.should_run('error', self.max_level):
            return

        return self.driver.error(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        if not self.driver.should_run('warning', self.max_level):
            return

        return self.driver.warning(message, *args, **kwargs)

    def notice(self, message, *args, **kwargs):
        if not self.driver.should_run('notice', self.max_level):
            return

        return self.driver.notice(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        if not self.driver.should_run('info', self.max_level):
            return

        return self.driver.info(message, *args, **kwargs)
        
    def debug(self, message, *args, **kwargs):
        if not self.driver.should_run('debug', self.max_level):
            return

        return self.driver.debug(message, *args, **kwargs)

    def channel(self, channel):
        from ..ChannelFactory import ChannelFactory
        return ChannelFactory().make(channel)()