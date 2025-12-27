import pendulum
from fastapi_startkit.facades import Config

class MultiBaseChannel:

    def get_time(self):
        return pendulum.now().in_tz(Config.get('logging.channels.timezone', 'UTC'))

    def emergency(self, message, *args, **kwargs):
        for channel in self.channels:
            if not channel.driver.should_run('emergency', channel.max_level):
                continue
            
            channel.driver.emergency(message, *args, **kwargs)

    def alert(self, message, *args, **kwargs):
        for channel in self.channels:
            if not channel.driver.should_run('alert', channel.max_level):
                continue
            
            channel.driver.alert(message, *args, **kwargs)
            
    def critical(self, message, *args, **kwargs):
        for channel in self.channels:
            if not channel.driver.should_run('critical', channel.max_level):
                continue
            
            channel.driver.critical(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        for channel in self.channels:
            if not channel.driver.should_run('error', channel.max_level):
                continue
            
            channel.driver.error(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        for channel in self.channels:
            if not channel.driver.should_run('warning', channel.max_level):
                continue
            
            channel.driver.warning(message, *args, **kwargs)

    def notice(self, message, *args, **kwargs):
        for channel in self.channels:
            if not channel.driver.should_run('notice', channel.max_level):
                continue
            
            channel.driver.notice(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        for channel in self.channels:
            if not channel.driver.should_run('info', channel.max_level):
                continue
            
            channel.driver.info(message, *args, **kwargs)
        
    def debug(self, message, *args, **kwargs):
        for channel in self.channels:
            if not channel.driver.should_run('debug', channel.max_level):
                continue
            
            channel.driver.debug(message, *args, **kwargs)

