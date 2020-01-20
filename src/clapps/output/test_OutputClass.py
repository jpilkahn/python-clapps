#!/usr/bin/env python3


from contextlib import contextmanager
from io import StringIO
from logging import (
    getLogger,
    StreamHandler,
)
from sys import stderr
from uuid import uuid4
from unittest import (
    main,
    TestCase,
)

from clapps.output import (
    LogLevel,
    OutputClass,
)

__all__ = ["TestLoggingMethod"]


# ----------------------------------- util ------------------------------------

@contextmanager
def mockIo():
    originalStreams = []

    class MockStream(object):
        def __init__(self, name):
            self.name = name
            self.stream = StringIO()

    class MockIo(object):
        stderr = MockStream("stderr")
        stdout = MockStream("stdout")

    _mockIo = MockIo()

    def doForStreamHandler(function):
        rootLogger = getLogger()
        for handler in rootLogger.handlers:
            if isinstance(handler, StreamHandler):
                function(handler)

    def addMockStream(handler):
        originalStreams.append(handler.stream)
        if handler.stream is stderr:
            handler.stream = _mockIo.stderr.stream
        else:
            handler.stream = _mockIo.stdout.stream

    def resetStream(handler):
        handler.stream = originalStreams.pop(0)

    doForStreamHandler(addMockStream)

    try:
        yield _mockIo
    finally:
        doForStreamHandler(resetStream)


# ----------------------------------- tests -----------------------------------

class TestLoggingMethods(TestCase):
    expectedLogLevelThresholdOutErr = LogLevel.Warning

    def test_loggingMethods(self):
        for methodLogLevel in LogLevel:
            if methodLogLevel is LogLevel.NotSet:
                # `NotSet` has no corresponding method.
                continue

            for appLogLevel in LogLevel:
                methodName = methodLogLevel.name.lower()

                with self.subTest(
                    method=f"OutputClass.{methodName}",
                    logLevel=appLogLevel.name
                ):
                    self.__test_LoggingMethod(
                        methodName,
                        methodLogLevel,
                        appLogLevel
                    )

    def __test_LoggingMethod(
        self,
        methodName,
        methodLogLevel,
        appLogLevel
    ):
        outputClass = OutputClass(logLevel=appLogLevel)
        method = getattr(
            outputClass,
            methodName
        )

        message = str(uuid4())

        def assertMessage(mockStream):
            output = mockStream.stream.getvalue()
            self.assertIn(
                message,
                output,
                msg=(
                    "Expected message not found in output on "
                    f"{mockStream.name}."
                )
            )

        def assertNoOutput(mockStream):
            self.assertEqual(
                mockStream.stream.getvalue(),
                "",
                msg=f"Unepected output on {mockStream.name}."
            )

        with mockIo() as io:
            method(message)

            if methodLogLevel < appLogLevel:
                assertNoOutput(io.stderr)
                assertNoOutput(io.stdout)
            else:
                if methodLogLevel < self.expectedLogLevelThresholdOutErr:
                    assertMessage(io.stdout)
                    assertNoOutput(io.stderr)
                else:
                    assertMessage(io.stderr)
                    assertNoOutput(io.stdout)


if __name__ == '__main__':
    main()
