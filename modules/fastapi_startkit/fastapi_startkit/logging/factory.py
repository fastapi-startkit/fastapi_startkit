from .drivers import LogSingleDriver, LogTerminalDriver, LogSlackDriver, LogSyslogDriver
class DriverFactory:

    drivers = {
        'single': LogSingleDriver,
        'daily': LogSingleDriver,
        'slack': LogSlackDriver,
        'syslog': LogSyslogDriver,
        'terminal': LogTerminalDriver
    }

    @classmethod
    def make(cls, driver):
        return cls.drivers.get(driver)

