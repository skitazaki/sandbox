#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Use "inspect" module.
# usage:
# $ python d50.py

import inspect


def func1():
    """function No.1.
    do nothing special.
    """
    print __doc__


def func2():
    """function No.2.
    of course, do nothing special, too.
    """
    print __file__

FUNCTIONS = [func1, func2]


def main():
    for f in FUNCTIONS:
        print "%s defined in %s" % (f, inspect.getfile(f))
        print inspect.getdoc(f)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
