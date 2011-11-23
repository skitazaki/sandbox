#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Misc. utilities.
Use these after copying to your projects.

:Author: KITAZAKI Shigeru
"""

import datetime
import logging
import os
import optparse


class ArgumentError(Exception):
    pass


def parse_args(doc=None, prefook=None, postfook=None):
    """Sets up logging verbosity.

    :rtype: normal arguments except options.
    """
    parser = optparse.OptionParser(doc)
    parser.add_option("-f", "--file", dest="filename",
        help="setting file", metavar="FILE")
    parser.add_option("-o", "--out", dest="output",
        help="output file", metavar="FILE")
    parser.add_option("--basedir", dest="basedir",
        help="base directory", default=os.getcwd())
    parser.add_option("-v", "--verbose", dest="verbose",
        default=False, action="store_true", help="verbose mode")
    parser.add_option("-q", "--quiet", dest="quiet",
        default=False, action="store_true", help="quiet mode")

    if prefook:
        prefook(parser)

    opts, args = parser.parse_args()

    if postfook:
        try:
            postfook(opts, args)
        except ArgumentError, e:
            parser.error(e)

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)
    elif not opts.quiet:
        logging.basicConfig(level=logging.INFO)

    return opts, args


def check_file_path(opts, files):
    if opts.filename and not os.path.exists(opts.filename):
        raise ArgumentError("Configuration file was not found.")
    if opts.output and os.path.exists(opts.output):
        logging.warn("\"%s\" already exists.", opts.output)

    if not files:
        raise ArgumentError("No input file.")
    notfound = filter(lambda f: not os.path.exists(f), files)
    if notfound:
        raise ArgumentError("File not found: " + ','.join(notfound))


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
