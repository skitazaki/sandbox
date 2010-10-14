#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Duff's Device for loop processing.
# usage:
# $ python d51.py

import time

LOOP_COUNT = 1000000

def process(item):
  """No meaning.
  """
  return item["num"] + item["num"] * item["num"] + item["num"]

def gendata():
  dt = []
  for i in range(LOOP_COUNT):
    dt.append({"num":i})
  return dt

def main():
  start = time.clock()
  data = gendata()
  print "Data amount: %d, time:%f" % (len(data), time.clock() - start)
  start = time.clock()
  for item in data:
    process(item)
  print "naive loop time: %f" % (time.clock() - start)
  start = time.clock()
  length = len(data)
  n = length % 8
  for i in range(n):
    process(data[length - i])
  n = length - n - 1
  while n > 0:
    # Python does NOT allow increment / decrement operations.
    process(data[n])
    n -= 1
    process(data[n])
    n -= 1
    process(data[n])
    n -= 1
    process(data[n])
    n -= 1
    process(data[n])
    n -= 1
    process(data[n])
    n -= 1
    process(data[n])
    n -= 1
    process(data[n])
    n -= 1
  print "Another loop time: %f" % (time.clock() - start)

if __name__ == '__main__':
  main()

# vim: set expandtab tabstop=2 shiftwidth=2 cindent :

