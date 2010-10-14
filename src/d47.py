#!/usr/bin/env python
# -*- coding: utf-8 -*-
# use "doctest" module
# more test modules are listed [here](http://packages.python.org/testing/)
# usage:
# $ python d47.py -v

def recursive(query):
  """print from backward.
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
  """print from forward.
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

# vim: set expandtab tabstop=2 shiftwidth=2 cindent :

