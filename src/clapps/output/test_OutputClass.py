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

    def test_isSilent(self):
        self.__iterLoggingMethods(self.__test_isSilent)

    def test_Output(self):
        self.__iterLoggingMethods(self.__test_Output)

    def assertMessageIn(self, message, mockStream):
        output = mockStream.stream.getvalue()
        self.assertIn(
            message,
            output,
            msg=(
                "Expected message not found in output on "
                f"{mockStream.name}."
            )
        )

    def assertNoOutput(self, mockStream):
        self.assertEqual(
            mockStream.stream.getvalue(),
            "",
            msg=f"Unepected output on {mockStream.name}."
        )

    def __iterLoggingMethods(self, test):
        for methodLogLevel in LogLevel:
            # `NotSet` has no corresponding method.
            if methodLogLevel is LogLevel.NotSet:
                continue

            for appLogLevel in LogLevel:
                methodName = methodLogLevel.name.lower()

                with self.subTest(
                    method=f"OutputClass.{methodName}",
                    logLevel=appLogLevel.name
                ):
                    test(
                        methodName,
                        methodLogLevel,
                        appLogLevel
                    )

    def __test_Output(
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

        with mockIo() as io:
            method(message)

            if methodLogLevel < appLogLevel:
                self.assertNoOutput(io.stderr)
                self.assertNoOutput(io.stdout)
            else:
                if methodLogLevel < self.expectedLogLevelThresholdOutErr:
                    self.assertMessageIn(message, io.stdout)
                    self.assertNoOutput(io.stderr)
                else:
                    self.assertMessageIn(message, io.stderr)
                    self.assertNoOutput(io.stdout)

    def __test_isSilent(
        self,
        methodName,
        methodLogLevel,
        appLogLevel
    ):
        outputClass = OutputClass(
            isSilent=True,
            logLevel=appLogLevel
        )
        method = getattr(
            outputClass,
            methodName
        )

        message = str(uuid4())

        with mockIo() as io:
            method(message)

            self.assertNoOutput(io.stderr)
            self.assertNoOutput(io.stdout)


class TestOutFile(TestCase):
    # TODO
    pass


class TestResultOutput(TestCase):
    # TODO
    pass


class TestSilent(TestCase):
    # TODO
    pass


if __name__ == '__main__':
    main()
