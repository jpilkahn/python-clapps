#!/usr/bin/env python3


from logging import (
    FileHandler,
    Formatter,
    getLogger,
    StreamHandler,
)
from pathlib import Path
from sys import stdout

from clapps.output.LogLevel import LogLevel


__all__ = ["OutputClass"]


class OutputClass(object):
    @property
    def logLevel(self):
        return self._logLevel

    @logLevel.setter
    def logLevel(self, level):
        self._logLevel = LogLevel(level)
        getLogger().setLevel(self._logLevel.value)

    @property
    def isSilent(self):
        return self._isSilent

    @isSilent.setter
    def isSilent(self, value):
        def silentFilter():
            return 0

        if not isinstance(value, bool):
            raise TypeError("isSilent is a boolean switch.")

        self._isSilent = value

        if value:
            self._resultHandlerStdout.addFilter(silentFilter)
        else:
            self._resultHandlerStdout.removeFilter(silentFilter)

    @property
    def outFile(self):
        return str(self._outFile)

    @outFile.setter
    def outFile(self, filename):
        resultLogger = self.__getResultLogger()

        if self._resultHandlerOutFile is not None:
            resultLogger.removeHandler(self._resultHandlerOutFile)

        if filename is None:
            self._outFile = None
            return

        path = Path(filename)

        try:
            with path.open("r+"):
                pass
        except Exception as e:
            self.exception(
                f"{str(path.resolve())} could not be opened for writing."
            )

        self._outFile = path
        self._resultHandlerOutFile = FileHandler(
            path,
            mode="a",
            delay=True
        )
        resultLogger.addHandler(self._resultHandlerOutFile)

    def __init__(
        self,
        isSilent=False,
        logLevel=LogLevel.Warning,
        outFile=None
    ):
        self._resultFormatter = Formatter(
            fmt="{message}",
            style="{"
        )
        self._resultHandlerStdout = StreamHandler(stdout)
        self._resultHandlerStdout.setFormatter(self._resultFormatter)
        self.__getResultLogger().addHandler(self._resultHandlerStdout)

        self.isSilent = isSilent
        self.logLevel = logLevel

    def debug(self, msg):
        getLogger().debug(msg)

    def info(self, msg):
        getLogger().info(msg)

    def warning(self, msg):
        getLogger().warning(msg)

    def error(self, msg):
        getLogger().error(msg)

    def exception(self, msg):
        getLogger().exception(msg)

    def critical(self, msg):
        getLogger().critical(msg)

    def result(self, msg):
        self.__getResultLogger().info(msg)

    def __getResultLogger(self):
        return getLogger("result")
