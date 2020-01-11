#!/usr/bin/env python3


__title__ = 'clapps - Command Line App Skeleton'
__version__ = '0.0.0'


from clapps.output import OutputClass


output = OutputClass()


def main():
    output.warning("OK")
