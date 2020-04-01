# -*- coding: utf-8 -*-

"""Misc. utilities on a sandbox project.
"""

__title__ = "sandboxlib"
__version__ = "0.0.2"
__author__ = "Shigeru Kitazaki"

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
    boilerplate = '''# -*- coding: utf-8 -*-

"""Description is here.
"""

import logging
import sys

import click

from sandboxlib import main


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


@main.command("run")
@click.argument("file", type=click.File("r"), nargs=-1)
def run(file):
    writer = None
    p = Processor(writer)
    for fh in file:
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
