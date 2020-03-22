#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog {module}

Run profiler, see Chapter 12 of Expert Python Programming.
"""

import logging
import cProfile

from sandboxlib import parse_args

RUN_FUNCTION = 'main'


def run_profiler(func):
    profiler = cProfile.Profile()
    profiler.runcall(func)
    profiler.print_stats()


def main():
    options, args = parse_args(doc=__doc__, minargc=1)
    for m in args:
        module = __import__(m)
        if hasattr(module, RUN_FUNCTION):
            func = getattr(module, RUN_FUNCTION)
            run_profiler(func)
        else:
            logging.error("No '%s' is found in %s.", RUN_FUNCTION, m)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
