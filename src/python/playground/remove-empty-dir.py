# -*- coding: utf-8 -*-

"""
Removes all empty directories.
"""

import logging
import os

import click

from sandboxlib import main


def removeemptydir(root) -> int:
    """Removes directory which is empty or has only one hidden file."""
    logger = logging.getLogger("")
    removed = 0
    for dirname, dirs, files in os.walk(root):
        if len(dirs) == 0 and (
            len(files) == 0 or (len(files) == 1 and files[0].startswith("."))
        ):
            answer = input(f'remove: "{dirname}" [y/N] ')
            if answer == "y":
                [os.unlink(os.path.join(dirname, f)) for f in files]
                os.rmdir(dirname)
                removed += 1
                logger.info(f"removed {dirname}")
    if removed > 0:
        logger.info(f"removed {removed} directories under {root}")
    return removed


@main.command("run")
@click.argument("directory", type=click.Path(exists=True), nargs=-1)
def run(directory):
    removed = 0
    for d in directory:
        removed += removeemptydir(d)
    if removed > 0:
        click.echo(f"removed {removed} directories")


if __name__ == "__main__":
    main()
