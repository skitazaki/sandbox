# -*- coding: utf-8 -*-

"""
Run profiler, see Chapter 12 of Expert Python Programming.
"""

import logging
import cProfile

from sandboxlib import parse_args

RUN_FUNCTION = 'test'


def run_profiler(func):
    profiler = cProfile.Profile()
    profiler.runcall(func)
    profiler.print_stats()


def setup_arguments(parser):
    parser.add_argument("modules", nargs="*", help="module names")


def main():
    args = parse_args(doc=__doc__, prehook=setup_arguments)
    modules = args.modules
    for m in modules:
        module = __import__(m)
        if hasattr(module, RUN_FUNCTION):
            func = getattr(module, RUN_FUNCTION)
            run_profiler(func)
        else:
            logging.error(f'No "{RUN_FUNCTION}" is found in "{m}".')

if __name__ == '__main__':
    main()
