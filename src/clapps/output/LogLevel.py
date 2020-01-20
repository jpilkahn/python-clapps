"""
@enum LogLevel
The Python standard library's [`logging`][logging] module's default
[log levels][levels], accessible as an enumeration.

[levels]: https://docs.python.org/3/library/logging.html#levels
          "logging module documentation: 'Logging Levels'"

[logging]: https://docs.python.org/3/library/logging.html
           "logging module documentation"
"""

from enum import IntEnum
from logging import (
    NOTSET,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
)


class LogLevel(IntEnum):
    NotSet = NOTSET
    Debug = DEBUG
    Info = INFO
    Warning = WARNING
    Error = ERROR
    Critical = CRITICAL
