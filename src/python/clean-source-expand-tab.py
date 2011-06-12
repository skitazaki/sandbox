#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Expands tab to 4-whitespace and removes trailing whitespaces.

import os
import os.path
import re
import sys


def usage(program):
    print '''usage: python %s [file ...]
    ''' % (program)
    sys.exit(1)

tabs = re.compile("\t")
WHITESPACE = " " * 4    # 4-whitespace


def cleanfile(fname):
    if os.path.isfile(fname):
        tmp = open("%s.tmp" % fname, 'w')
        for l in open(fname):
            tmp.write(tabs.sub(WHITESPACE, l).rstrip() + "\n")
        tmp.close()
        os.rename(tmp.name, fname)
    else:
        print("[ERROR] '%s' is not a valid file." % fname)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage(sys.argv[0])
    for fname in sys.argv[1:]:
        cleanfile(fname)

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
