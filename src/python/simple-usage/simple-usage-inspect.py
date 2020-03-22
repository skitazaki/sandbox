#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options]

Use "inspect" module.
"""

import inspect


def func1():
    """Function No.1.
    do nothing special.
    """
    print __doc__


def func2():
    """Function No.2.
    of course, do nothing special, too.
    """
    print __file__

FUNCTIONS = [func1, func2]


def main():
    for f in FUNCTIONS:
        print "-" * 78
        print "-->", f.__name__, "<--"
        print "%s defined in %s" % (f, inspect.getfile(f))
        print "Arguments:", inspect.getargspec(f)
        print inspect.getdoc(f)
        print "Invoke!!"
        f()

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
