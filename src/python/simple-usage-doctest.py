#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options]

Use "doctest" module.
More test modules are listed at <http://packages.python.org/testing/>
"""


def recursive(query):
    """Print from backward.
    >>> recursive("hoge")
    e
    ge
    oge
    hoge
    """
    if len(query):
        recursive(query[1:])
        print query


def generative(query):
    """Print from forward.
    >>> generative("hoge")
    h
    ho
    hog
    hoge
    """

    def gen(q):
        while len(q):
            yield q[0]
            q = q[1:]

    s = ""
    for i in gen(query):
        s += i
        print s

if __name__ == '__main__':
    import doctest
    doctest.testmod()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
