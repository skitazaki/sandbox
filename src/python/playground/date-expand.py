#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Expand date string

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

    $ python date-expand.py -v
    DEBUG:root:Start: 2012-11-05
    20121105
"""

import argparse
import datetime
import logging
import sys

TODAY = datetime.date.today()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, default=TODAY.year)
    parser.add_argument('--month', type=int, default=TODAY.month)
    parser.add_argument('--day', type=int, default=TODAY.day)
    parser.add_argument('--format', default='%Y%m%d')
    parser.add_argument('--days', type=int, default=1)
    parser.add_argument('--reverse', default=False, action="store_true")

    parser.add_argument('--output',
        type=argparse.FileType('w'), default=sys.stdout)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", dest="verbose",
                default=False, action="store_true",
                help="set logging to verbose mode")
    group.add_argument("-q", "--quiet", dest="quiet",
                default=False, action="store_true",
                help="set logging to quiet mode")

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    elif not args.quiet:
        logging.basicConfig(level=logging.INFO)

    s = datetime.date(args.year, args.month, args.day)
    logging.debug("Start: %s", s)
    for i in xrange(args.days):
        if args.reverse:
            t = s - datetime.timedelta(days=i)
        else:
            t = s + datetime.timedelta(days=i)
        args.output.write(t.strftime(args.format))
        args.output.write('\n')

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
