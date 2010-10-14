#!/usr/bin/env python
# -*- coding: utf-8 -*-
# use "inspect" module
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

FUNCTIONS = [ func1, func2 ]

def main():
  for f in FUNCTIONS:
    print "%s defined in %s" % (f, inspect.getfile(f))
    print inspect.getdoc(f)

if __name__ == '__main__':
  main()

# vim: set expandtab tabstop=2 shiftwidth=2 cindent :

