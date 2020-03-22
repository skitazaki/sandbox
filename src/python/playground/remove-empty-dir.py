# -*- coding: utf-8 -*-

"""
Removes all empty directories.
"""

import logging
import os
from pathlib import Path

from sandboxlib import parse_args


def removeemptydir(root):
    """removes directory which is empty or has only one hidden file."""
    for dirname, dirs, files in os.walk(root):
        if len(dirs) == 0 and (
            len(files) == 0 or (len(files) == 1 and files[0].startswith("."))
        ):
            answer = input(f'remove: "{dirname}" [y/N] ')
            if answer == "y":
                [os.unlink(os.path.join(dirname, f)) for f in files]
                os.rmdir(dirname)
                logging.info(f"removed {dirname}")


def setup_arguments(parser):
    parser.add_argument(
        "dirs", nargs="*", type=Path, help="directories", metavar="DIRECTORY"
    )


def main():
    args = parse_args(doc=__doc__, prehook=setup_arguments)
    dirs = args.dirs
    if dirs:
        [removeemptydir(d) for d in dirs]
    else:
        removeemptydir(Path.cwd())


if __name__ == "__main__":
    main()
