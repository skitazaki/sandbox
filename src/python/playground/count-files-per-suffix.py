# -*- coding: utf-8 -*-

"""
Get a count of how many file types a project has.
See <http://www.commandlinefu.com/commands/view/5386>
"""

import collections
import os
from pathlib import Path

import click

from sandboxlib import main

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


@main.command("run")
@click.argument("directory", type=click.Path(exists=True), nargs=-1)
def run(directory):
    for d in directory:
        filetypes(Path(d))


if __name__ == "__main__":
    main()
