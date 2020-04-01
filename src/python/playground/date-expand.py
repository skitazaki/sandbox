# -*- coding: utf-8 -*-

"""Expand date string

Examples::

    $ python date-expand.py
    20121105

    $ python date-expand.py --format="%Y-%m-%d"
    2012-11-05

    $ python date-expand.py --days=7
    20121105
    20121106
    20121107
    20121108
    20121109
    20121110
    20121111

    $ python date-expand.py --month=10 --day=1
    20121001

    $ python date-expand.py --month=9 --day=1 --days=30 --output date.dat
    $ head date.dat
    20120901
    20120902
    20120903
    20120904
    20120905
    20120906
    20120907
    20120908
    20120909
    20120910

    $ python date-expand.py --days=7 --reverse
    20121105
    20121104
    20121103
    20121102
    20121101
    20121031
    20121030

    $ python date-expand.py -vvv
    DEBUG:root:Start: 2012-11-05
    20121105
"""

import datetime
import logging

import click

from sandboxlib import main

TODAY = datetime.date.today()


@main.command("run")
@click.option("--year", type=int, default=TODAY.year)
@click.option("--month", type=int, default=TODAY.month)
@click.option("--day", type=int, default=TODAY.day)
@click.option("--format", default="%Y%m%d")
@click.option("--days", type=int, default=1)
@click.option("--reverse/--no-reverse", default=False)
@click.option("-o", "--output", help="path to output file", type=click.File("w"))
def run(year, month, day, format, days, reverse, output):
    s = datetime.date(year, month, day)
    logging.debug("Start: %s", s)
    for i in range(days):
        if reverse:
            t = s - datetime.timedelta(days=i)
        else:
            t = s + datetime.timedelta(days=i)
        if output:
            output.write(t.strftime(format))
            output.write("\n")
        else:
            click.echo(t.strftime(format))


if __name__ == "__main__":
    main()
