#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [dir1 [dir2 [ ... ]]]

Get a count of how many file types a project has.
See <http://www.commandlinefu.com/commands/view/5386>
"""

import collections
import os

from sandboxlib import parse_args

IGNORE_LIST = [".svn", ".git"]


def filetypes(proj):
    for dirname, dirs, files in os.walk(proj):
        if [d for d in IGNORE_LIST if dirname.find(d) >= 0]:
            continue
        types = collections.defaultdict(int)
        for f in files:
            try:
                types[os.path.splitext(f)[1]] += 1
            except KeyError:
                pass
        print("%s" % dirname)
        for t in types:
            print("%16s%4d" % (t, types.get(t)))


def main():
    opts, args = parse_args(doc=__doc__)
    if args:
        [filetypes(d) for d in args]
    else:
        filetypes(os.getcwd())

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :