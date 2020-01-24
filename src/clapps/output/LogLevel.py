"""
@enum LogLevel
The Python standard library's [`logging`][logging] module's default
[log levels][levels], accessible as an enumeration.

[levels]: https://docs.python.org/3/library/logging.html#levels
          "logging module documentation: 'Logging Levels'"

[logging]: https://docs.python.org/3/library/logging.html
           "logging module documentation"
"""

from enum import (
    Enum,
    IntEnum,
)
from logging import (
    NOTSET,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
)


__all__ = ["LogLevel"]


class EnumConstructibleFromName(Enum):
    @classmethod
    def _missing_(cls, value):
        if type(value) is str:
            value = value.lower()
            for member in cls:
                if member.name.lower() == value:
                    return cls(member.value)
                    break

        super()._missing_(value)


class LogLevel(EnumConstructibleFromName, IntEnum):
    NotSet = NOTSET
    Debug = DEBUG
    Info = INFO
    Warning = WARNING
    Error = ERROR
    Critical = CRITICAL
