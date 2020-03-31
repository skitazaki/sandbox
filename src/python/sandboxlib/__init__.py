# -*- coding: utf-8 -*-

"""Misc. utilities on a sandbox project.
"""

__title__ = "sandboxlib"
__version__ = "0.0.1"
__author__ = "Shigeru Kitazaki"

import argparse
import datetime
import logging
import logging.config
from pathlib import Path

import click

DEFAULT_ENCODING = "utf-8"

logger = logging.getLogger("sandbox")


DEFAULT_LOGGING_DIRECTORY = Path.cwd()
DEFAULT_LOGGING_FILENAME = "sandbox.log"

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
        "detailed": {
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "%(asctime)s [%(levelname)s] %(name)s "
            "%(filename)s:L%(lineno)-4d: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "stream": "ext://sys.stderr",
            "formatter": "standard",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": str(DEFAULT_LOGGING_DIRECTORY / DEFAULT_LOGGING_FILENAME),
            "mode": "a",
            "maxBytes": 10485760,
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "ERROR", "propagate": True},
        "sandbox": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


def configure_logging(
    logging_settings: dict = None,
    verbose: int = 0,
    quiet: bool = False,
    logger: str = "sandbox",
):
    logging.config.dictConfig(DEFAULT_LOGGING)
    if logging_settings:
        logging.config.dictConfig(logging_settings)
    if quiet or verbose > 0:
        if isinstance(logger, str):
            logger = logging.getLogger(logger)
        if quiet:
            logger.setLevel(logging.CRITICAL)
        elif verbose >= 3:
            logger.setLevel(logging.DEBUG)
        elif verbose >= 2:
            logger.setLevel(logging.INFO)
        elif verbose >= 1:
            logger.setLevel(logging.WARN)


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
        "-c",
        "--config",
        dest="config",
        help="configuration file",
        metavar="FILE",
        type=Path,
    )

    loglevel_option = parser.add_mutually_exclusive_group()

    loglevel_option.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        dest="verbose",
        help="increase logging verbosity",
    )

    loglevel_option.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        dest="quiet",
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

    if args.config and not args.config.exists():
        parser.error("Configuration file was not found.")

    loglevel = None
    if args.quiet:
        loglevel = "CRITICAL"
    elif args.verbose >= 3:
        loglevel = "DEBUG"
    elif args.verbose >= 2:
        loglevel = "INFO"
    elif args.verbose >= 1:
        loglevel = "WARN"

    logging_settings = None
    if loglevel:
        logging_settings = DEFAULT_LOGGING.copy()
        logging_settings["loggers"][""]["level"] = loglevel
    configure_logging(logging_settings)

    return args


def setup_fileio(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        help="path to output file",
        metavar="FILE",
        type=Path,
    )
    parser.add_argument(
        "--input-encoding",
        default=DEFAULT_ENCODING,
        dest="enc_in",
        help="encoding of input source",
        metavar="ENCODING",
    )
    parser.add_argument(
        "--output-encoding",
        default=DEFAULT_ENCODING,
        dest="enc_out",
        help="encoding of output destination",
        metavar="ENCODING",
    )

    parser.add_argument(
        "files",
        help="list of paths of input files",
        metavar="FILE",
        nargs="*",
        type=Path,
    )


def check_file_path(args):
    if args.output and args.output.exists():
        logger.warn('"%s" already exists.', args.output)

    files = args.files
    if not files:
        raise ArgumentError("No input file.")
    notfound = list(filter(lambda f: not f.exists(), files))
    if notfound:
        lst = list(map(str, notfound))
        raise ArgumentError("File not found: " + ",".join(lst))


@click.group()
@click.option(
    "-c", "--config", help="Path to configuration file", type=click.Path(exists=True),
)
@click.option("-v", "--verbose", count=True, help="Increase logging verbosity")
@click.option(
    "-q", "--quiet/--no-quiet", is_flag=True, help="Set logging to quiet mode"
)
@click.pass_context
def main(ctx, config, verbose, quiet):
    configure_logging(verbose=verbose, quiet=quiet)


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

logging.getLogger(__name__).addHandler(logging.NullHandler())


if __name__ == "__main__":
    boilerplate = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Description is here.
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


def test_process():
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
