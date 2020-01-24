#!/usr/bin/env python3


from argparse import ArgumentParser

from clapps.output import (
    LogLevel,
    OutputClass
)


__all__ = ["CliAppSkeleton"]


class Skeleton(OutputClass):
    _args = None

    def __init__(self):
        self._argumentParser = ArgumentParser(description="CLI App Skeleton")

        self.addArgument(
            "--log-level",
            action="store",
            help="Log level. (Does not affect primary output.)",
            type=LogLevel,
            choices=[
                level.name for level in LogLevel if level is not LogLevel.NotSet
            ],
            default=LogLevel.Warning,
            dest="logLevel"
        )

        self.addArgument(
            "-o", "--out-file",
            help="Path to file to save output to.",
            action="store",
            dest="outFile"
        )

        self.addArgument(
            "-s", "--silent",
            help=(
                "No output."
                "(Does not apply to a file specified via the `-o` flag.)"
            ),
            action="store_true",
            dest="isSilent"
        )

        super().__init__(**self.args.__dict__)

    def impl(self):
        raise NotImplementedError("Must implement impl()")

    @property
    def args(self):
        if not self._args:
            self._args = self.__parseArgs()

        return self._args

    def addArgument(self, *args, **kwargs):
        self._argumentParser.add_argument(*args, **kwargs)
        self._args = None

    def run(self):
        try:
            self.impl()
        except Exception as e:
            if not self.args.silent:
                self.exception("Fatal error:")

    def __parseArgs(self):
        return self._argumentParser.parse_args()
