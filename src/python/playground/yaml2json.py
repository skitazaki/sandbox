# -*- coding: utf-8 -*-

"""Convert data format from YAML to JSON.
"""

import logging
import json

import click
import yaml
import yaml.scanner

from sandboxlib import main


@main.command("run")
@click.argument("file", type=click.File("r"), nargs=-1)
def yaml2json(file):
    logger = logging.getLogger("")
    for fh in file:
        try:
            cfg = yaml.safe_load(fh)
        except yaml.scanner.ScannerError as e:
            logger.error(f"Invalid YAML file: {e}")
            continue
        click.echo(json.dumps(cfg, indent=2))


if __name__ == "__main__":
    main()
