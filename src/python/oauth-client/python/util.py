#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""\\
Misc. utilities.
Use these after copying to your projects.

:Author: KITAZAKI Shigeru
"""

import datetime
import logging
import optparse


def parse_args():
    """Sets up logging verbosity.

    :rtype: normal arguments except options.
    """
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", dest="filename",
        help="setting file", metavar="FILE")
    parser.add_option("-v", "--verbose", dest="verbose",
        default=False, action="store_true", help="verbose mode")
    parser.add_option("-q", "--quiet", dest="verbose",
        default=True, action="store_false", help="quiet mode")

    opts, args = parser.parse_args()

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)

    return opts, args


def load_object(path):
    dot = path.rindex('.')
    module_name, obj_name = path[:dot], path[dot + 1:]
    # TODO error handling.
    module = __import__(module_name, '', '', [''])
    obj = getattr(module, obj_name)
    return obj

ZERO = datetime.timedelta(0)


class UTC(datetime.tzinfo):
    """Representation of `UTC` timezone."""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

NOW = datetime.datetime.now(UTC())

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
