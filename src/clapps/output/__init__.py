#!/usr/bin/env python3


from enum import (
    auto,
    Enum,
)
from logging import (
    Formatter,
    getLogger,
    StreamHandler,
    NOTSET,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
)
from sys import (
    stderr,
    stdout,
)
from time import gmtime

from clapps.output.LogLevel import LogLevel


__all__ = [
    "LogLevel"
]


# ---------------------------------- format -----------------------------------

style = "{"


# ------------------------------- format: time --------------------------------


class ReferenceTime(Enum):
    def __str__(self):
        return self.value

    absolute = "{asctime}"
    relative = "f'{msecs:%H:%M:%S.sss}'"


# Applies to `ReferenceTime.absolute` / `asctime`,
# set on the `logging.Formatter` instance during initialization.
dateFormat = "%Y-%m-%d"
timeFormat = "%H:%M:%S"
timezoneFormat = "%z (%Z)"
datetimeFormat = f"{dateFormat} {timeFormat} {timezoneFormat}"


class UtcFormatter(Formatter):
    converter = gmtime


# ---------------------------- format: log record -----------------------------

prefixedMessage = f"{ReferenceTime.absolute}{': [{levelname}] {message}'}"
sourceInfo = "{module} ({process})"

fmt = f"{prefixedMessage}\n{sourceInfo}"

utcFormatter = UtcFormatter(
    fmt=fmt,
    datefmt=datetimeFormat,
    style=style
)


# ---------------------------- initialize logging -----------------------------

rootLogger = getLogger()

# Unset log level on the root Logger instance (`WARNING` by default).
# - Let individual handlers filter on the basis of level, depending on
#   (a) their responsibility and (b) the currently set cmdline args.
# - Adjust on using class' initialization.
rootLogger.setLevel(NOTSET)

# Let `WARNING` (numeric value 30) be the threshold between stdout & stderr.
logLevelThresholdOutErr = WARNING

stderrHandler = StreamHandler(stderr)
stdoutHandler = StreamHandler(stdout)

stderrHandler.setLevel(logLevelThresholdOutErr)
stdoutHandler.setLevel(NOTSET)
stdoutHandler.addFilter(
    lambda record: 1 if record.levelno < logLevelThresholdOutErr else 0
)

stderrHandler.setFormatter(utcFormatter)
stdoutHandler.setFormatter(utcFormatter)

rootLogger.addHandler(stderrHandler)
rootLogger.addHandler(stdoutHandler)
