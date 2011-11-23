#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options] [dir1 [dir2 [ ... ]]]

Removes all empty directories.
"""

import logging
import os

from sandboxlib import parse_args


def removeemptydir(root):
    """removes directory which is empty or has only one hidden file."""
    for dirname, dirs, files in os.walk(root):
        if len(dirs) == 0 and (len(files) == 0 or
              (len(files) == 1 and files[0].startswith("."))):
            answer = raw_input("remove: '%s' [y/N] " % dirname)
            if answer == "y":
                [os.unlink(os.path.join(dirname, f)) for f in files]
                os.rmdir(dirname)
                logging.info("removed %s", dirname)


def main():
    opts, dirs = parse_args(doc=__doc__)
    if dirs:
        [removeemptydir(d) for d in dirs]
    else:
        removeemptydir(os.getcwd())

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
