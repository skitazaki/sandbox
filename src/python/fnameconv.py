#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""File name convert script for Google takeout.
(mainly for Google Buzz export)
"""

import os
import shutil
from datetime import datetime


def determine_new_file_name(timestamp, suffix):
    mtime = datetime.fromtimestamp(timestamp)
    base = mtime.strftime('%Y-%m-%d-%H-%M-%S')
    c = 0
    while True:
        if c:
            cand = "%s.%d%s" % (base, c, suffix)
        else:
            cand = base + suffix
        if not os.path.exists(cand):
            return cand
        c += 1


def fnameconv(basedir, outputdir=None):
    outputdir = outputdir or basedir
    if not os.path.exists(outputdir):
        raise SystemExit("\"%s\" is not found." % (outputdir,))
    for f in os.listdir(basedir):
        # XXX: ignore list should be optional argument
        if f == __file__:
            continue
        fname = os.path.join(basedir, f)
        _, suffix = os.path.splitext(fname)
        cand = determine_new_file_name(os.stat(fname).st_mtime, suffix)
        dst = os.path.join(outputdir, cand)
        shutil.move(fname, dst)


def main():
    # XXX: enable to pass from command-line argument
    basedir = '.'
    fnameconv(basedir)


def test():
    pass

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf8 :
