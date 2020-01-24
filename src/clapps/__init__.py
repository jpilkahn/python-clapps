#!/usr/bin/env python3


__title__ = 'clapps - Command Line App Skeleton'
__version__ = '0.0.0'


from clapps.Skeleton import Skeleton


__all__ = ["Skeleton"]


def main():
    app = Skeleton()
    app.warning("OK")
