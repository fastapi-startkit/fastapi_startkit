import dataclasses

from fastapi_startkit.environment import env
from fastapi_startkit.logging.config import StackChannel, DailyChannel, TerminalChannel


@dataclasses.dataclass
class LoggingConfig:
    default: str = dataclasses.field(default_factory=lambda: env('LOG_CHANNEL', 'stack'))

    channels: dict = dataclasses.field(default_factory=lambda: {
        'stack': StackChannel(
            driver='stack',
            channels=['daily', 'terminal']
        ),
        'daily': DailyChannel(
            level=env('LOG_DAILY_LEVEL', 'debug'),
            path=env('LOG_DAILY_PATH', 'storage/logs'),
        ),
        'terminal': TerminalChannel(
            level=env('LOG_TERMINAL_LEVEL', 'info'),
        ),
    })
