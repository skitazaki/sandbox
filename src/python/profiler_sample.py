#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """\
python %prog module_including_main

Run profiler, see Chapter 12 of Expert Python Programming.

Usage ::

    $ python profiler_sample.py d50
"""

import logging
import optparse
import cProfile

RUN_FUNCTION = 'main'


def parse_args():
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-v", "--verbose", dest="verbose",
            default=False, action="store_true", help="verbose mode")
    parser.add_option("-q", "--quiet", dest="verbose",
            default=True, action="store_false", help="quiet mode")

    opts, args = parser.parse_args()

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)

    return opts, args


def run_profiler(func):
    profiler = cProfile.Profile()
    profiler.runcall(func)
    profiler.print_stats()


def main():
    options, args = parse_args()
    if not args:
        raise SystemExit("No argements are given.")
    for m in args:
        module = __import__(m)
        if hasattr(module, RUN_FUNCTION):
            func = getattr(module, RUN_FUNCTION)
            run_profiler(func)
        else:
            logging.error("No '%s' is found in %s." % (RUN_FUNCTION, m))

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
