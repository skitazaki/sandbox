#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert plain text page to CSV file.

Jリーグ公式記録
* `J1 <http://www.j-league.or.jp/data/2/?league=j1>`_ (d104.J1.txt)
* `J2 <http://www.j-league.or.jp/data/2/?league=j2>`_ (d104.J2.txt)
"""

import csv
import sys
import os.path
import re
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class Match(object):

    fixture = None
    home = None
    away = None
    stadium = None
    kickoff = None
    tv = None

    def __init__(self, fixture, kickoff=None):
        self.fixture = fixture
        if kickoff:
            if kickoff.find('T') > 0:
                self.kickoff = kickoff[:kickoff.find('T')]
            else:
                self.kickoff = kickoff

    def set_date(self, date):
        self.kickoff = '2011-' + date.replace('/', '-')

    def set_time(self, time):
        self.kickoff += 'T' + time

    def to_row(self):
        ret = [self.fixture, self.home, self.away, self.stadium, self.kickoff]
        if self.tv:
            ret.append(self.tv)
        return ret

START = re.compile('第(?P<fixture>\d+)節')


def convert(fname, writer):
    io = StringIO()
    csvwriter = csv.writer(io)
    match = None
    for line in open(fname, 'rb'):
        row = line.strip().split()
        if len(row) == 2:
            match.set_date(row[0])
        elif len(row) == 3:
            m = re.search(START, row[0])
            match = Match(m.group('fixture'))
            match.set_date(row[1])
        elif len(row) > 3:
            if row[0].find(':') > 0:
                match.set_time(row[0])
                match.home = row[1]
                match.away = row[3]
                match.stadium = row[4]
                if len(row) > 5:
                    match.tv = row[5]
            else:
                match.home = row[0]
                match.away = row[2]
                match.stadium = row[3]
        else:
            continue
        if match and match.home and match.away:
            csvwriter.writerow(match.to_row())
            match = Match(match.fixture, match.kickoff)

    io.seek(0)
    writer.write(io.read())


def main():
    if len(sys.argv) != 2:
        print >>sys.stderr, "Give me file name from argument."
        sys.exit(1)
    fname = sys.argv[1]
    if not os.path.exists(fname):
        print >>sys.stderr, fname, "is not found."
        sys.exit(1)

    #writer = open('output.csv', 'wb')
    writer = sys.stdout
    convert(fname, writer)
    #writer.close()

if __name__ == "__main__":
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
