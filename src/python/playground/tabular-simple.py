#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Compose table data from row-based data.
Input format is Year, Month, Kind, and Value.
"""

import sys
import codecs
from collections import defaultdict
from itertools import imap, ifilter

ENCODING = 'utf-8'
DELIMITER = '\t'


class TabularContainer(object):

    def __init__(self, *header):
        self.header = header or ()
        self.data = []

    def add(self, row):
        self.data.append(row)

    def column(self, name):
        if name in self.header:
            idx = self.header.index(name)
            return imap(lambda r: r[idx] if len(r) > idx else None, self.data)

    def grouped(self, name):
        if name in self.header:
            data = defaultdict(list)
            idx = self.header.index(name)
            for d in self.data:
                data[d[idx]].append(dict(zip(self.header, d)))
            for k in sorted(data.keys()):
                yield (k, data[k])

    def __iter__(self):
        for d in self.data:
            yield dict(zip(self.header, d))


def main():
    fname = sys.argv[1]
    tc = TabularContainer('Key', 'Kind', 'Value')
    # Loading TSV data encoded with utf-8
    with codecs.open(fname, encoding=ENCODING) as fp:
        rows = imap(lambda line: line.strip().split(DELIMITER), fp)
        # Compose year and month fields as Key.
        [tc.add(('{0}-{1}'.format(r[0], r[1].zfill(2)), r[2], r[3]))
            for r in ifilter(lambda r: len(r) == 4, rows)]
    # Transform simple row data into tabular style based on Kind field
    kinds = sorted(set(tc.column('Kind')))
    transformed = []
    transformed.append(['Year', 'Month'] + kinds + ['Total', ])  # header
    for key, vals in tc.grouped('Key'):
        row = key.split('-')  # reverse procedure of adding phase
        d = {}
        for val in vals:
            d[val['Kind']] = val['Value']
        row += [d.get(k, '') for k in kinds]
        row.append(sum(map(int, [d.get(k, 0) for k in kinds])))
        transformed.append(row)
    # Calculate summation of column-based values
    total = {}
    for key, vals in tc.grouped('Kind'):
        total[key] = sum(map(int, [val['Value'] for val in vals]))
    row = ['Total', '']
    row += map(str, [total.get(k, '') for k in kinds])
    row.append(sum(total.values()))  # all of summation
    transformed.append(row)
    # Write out transfored tabular data as TSV style
    output = fname + '.out'
    with codecs.open(output, 'w', encoding=ENCODING) as fp:
        for t in transformed:
            fp.write(DELIMITER.join(map(unicode, t)))
            fp.write('\n')

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
