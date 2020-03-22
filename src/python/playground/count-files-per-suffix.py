# -*- coding: utf-8 -*-

"""
Get a count of how many file types a project has.
See <http://www.commandlinefu.com/commands/view/5386>
"""

import collections
import os
from pathlib import Path

from sandboxlib import parse_args

IGNORE_LIST = [".svn", ".git"]


def filetypes(proj: Path):
    for dirname, dirs, files in os.walk(proj):
        if [d for d in IGNORE_LIST if dirname.find(d) >= 0]:
            continue
        types = collections.defaultdict(int)
        for f in files:
            try:
                types[os.path.splitext(f)[1]] += 1
            except KeyError:
                pass
        print(dirname)
        for t in types:
            print(f"{t:>16}: {types.get(t)}")


def setup_arguments(parser):
    parser.add_argument(
        "dirs", nargs="*", type=Path, help="directories", metavar="DIRECTORY"
    )


def main():
    args = parse_args(doc=__doc__, prehook=setup_arguments)
    dirs = args.dirs
    if dirs:
        [filetypes(d) for d in dirs]
    else:
        filetypes(Path.cwd())


if __name__ == "__main__":
    main()
