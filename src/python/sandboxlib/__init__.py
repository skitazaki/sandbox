# -*- coding: utf-8 -*-

"""Misc. utilities on a sandbox project.
"""

__title__ = "sandboxlib"
__version__ = "0.0.1"
__author__ = "Shigeru Kitazaki"

import argparse
import datetime
import logging
import os

DEFAULT_ENCODING = "utf-8"
logger = logging.getLogger("sandbox")


def _init_logger():
    s = logging.StreamHandler()
    s.setFormatter(logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(s)


_init_logger()


class ArgumentError(Exception):
    pass


def parse_args(doc=None, prehook=None, posthook=None) -> argparse.Namespace:
    """Generic command line argument parser.
    * Handle configuration file and base directory.
    * Handle input and output encoding.
    * Sets up logging verbosity.

    :param doc string:
    :param prehook function:
    :param posthook function:
    :rtype: normal arguments except options.
    """
    parser = argparse.ArgumentParser(description=doc)
    parser.add_argument(
        "-f", "--file", dest="filename", help="setting file", metavar="FILE"
    )
    parser.add_argument(
        "--basedir", dest="basedir", help="base directory", default=os.getcwd()
    )

    loglevel = parser.add_mutually_exclusive_group()

    loglevel.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="count",
        default=0,
        help="increase logging verbosity",
    )

    loglevel.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        default=False,
        action="store_true",
        help="set logging to quiet mode",
    )

    if prehook:
        prehook(parser)

    args = parser.parse_args()

    if posthook:
        try:
            posthook(args)
        except ArgumentError as e:
            parser.error(e)

    if args.filename and not os.path.exists(args.filename):
        parser.error("Configuration file was not found.")

    if args.quiet:
        logger.setLevel(logging.CRITICAL)
    elif args.verbose >= 3:
        logger.setLevel(logging.DEBUG)
    elif args.verbose >= 2:
        logger.setLevel(logging.ERROR)
    elif args.verbose >= 1:
        logger.setLevel(logging.WARN)
    else:
        logger.setLevel(logging.INFO)

    return args


def setup_fileio(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-o", "--out", dest="output", help="output file", metavar="FILE"
    )
    parser.add_argument(
        "--input-encoding",
        dest="enc_in",
        help="encoding of input source",
        default=DEFAULT_ENCODING,
    )
    parser.add_argument(
        "--output-encoding",
        dest="enc_out",
        help="encoding of output destination",
        default=DEFAULT_ENCODING,
    )

    parser.add_argument("files", nargs="*", help="input files", metavar="FILE")


def check_file_path(args):
    if args.output and os.path.exists(args.output):
        logger.warn('"%s" already exists.', args.output)

    files = args.files
    if not files:
        raise ArgumentError("No input file.")
    notfound = filter(lambda f: not os.path.exists(f), files)
    if notfound:
        raise ArgumentError("File not found: " + ",".join(notfound))


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

if __name__ == "__main__":
    boilerplate = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options] file1 [file2 [ ... ]]

Description is here.
"""

import logging
import sys

from sandboxlib import parse_args, setup_fileio, check_file_path


class Processor(object):

    def __init__(self, writer=None):
        self.writer = writer or sys.stdout

    def process_file(self, fname, encoding):
        logging.info("Start processing: %s", fname)
        try:
            self.process(open(fname, encoding=encoding))
        except Exception as e:
            logging.error(e)
        logging.info("End processing: %s", fname)

    def process(self, stream):
        pass


def main():
    args = parse_args(doc=__doc__, prehook=setup_fileio, posthook=check_file_path)
    files = args.files
    writer = None
    if args.output:
        writer = open(args.output, 'w', args.enc_out)
    p = Processor(writer)
    for fname in files:
        p.process_file(fname, args.enc_in)
    if writer:
        writer.close()


def test():
    sample = """SAMPLE"""
    from cStringIO import StringIO
    io = StringIO()
    p = Processor(io)
    p.process(sample)
    io.seek(0)
    assert False

if __name__ == "__main__":
    main()
'''
    print(boilerplate)
