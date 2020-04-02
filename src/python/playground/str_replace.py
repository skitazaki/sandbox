# -*- coding: utf-8 -*-

"""Replace strings using a mapping file in CSV format.
"""

import csv
from functools import partial

import click

from sandboxlib import main


def mapper(patterns, line):
    s = line
    for ret, candidates in patterns.items():
        s = s.replace(candidates, ret)
    return s


@main.command("run")
@click.option(
    "-m",
    "--mapping",
    type=click.File("r"),
    required=True,
    help="path to a csv mapping file of target and candidates",
)
@click.argument("file", type=click.File("r"), nargs=-1)
def run(mapping, file):
    reader = csv.reader(mapping)
    next(reader)  # skip header line
    patterns = {}
    for r in reader:
        # Replace short name to full name in `jleague-clubnames.csv`
        patterns[r[0]] = r[1]
    func = partial(mapper, patterns)
    for fh in file:
        for line in fh:
            s = func(line)
            click.echo(s)


if __name__ == "__main__":
    main()
