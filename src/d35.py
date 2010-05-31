#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Sample usage of sqlite
# example:
# $ python d35.py -f d35.sqlite
# links:
# [http://docs.python.org/library/sqlite3.html]
# [http://net-newbie.com/sqlite/sqlite.html]

import getopt
import random
import sys
try:
  import sqlite3
except ImportError:
  print("Python 2.5 or higher required.")
  sys.exit(1)

# NOTE: set this value from command line argument.
DATA_AMOUNT = 50

# enumeration for generating sample data
TRANS_TYPE = ("BUY", "SELL")
SYMBOL_TYPE = ("Apple", "Google", "Microsoft", "Sony")

def parse_args():
  usage = """usage: python %s [-f database file]
Options:
  -f database file name (if none, use :memory:)
  """
  try:
    opts, args = getopt.getopt(sys.argv[1:], "f:h")
  except getopt.GetoptError:
    print(usage % (sys.argv[0]))
    sys.exit(1)
  fname = ":memory:"
  for o,v in opts:
    if o == "-f":
      fname = v
    if o == "-h":
      print(usage % (sys.argv[0]))
      sys.exit(0)
  return fname

def createtable(cur):
  cur.execute("""SELECT sql FROM sqlite_master
      WHERE type='table' AND tbl_name='stocks'""")
  r = cur.fetchone()
  # NOTE: output should be printed only when verbose mode.
  if r:
    print('"stocks" is already created: %s' % r)
  else:
    # it's okay to use "IF NOT EXISTS", but checking current status is more
    # user-friendly to avoid to overwrite current data.
    cur.execute("""CREATE TABLE stocks (
      date TEXT, trans TEXT, symbol TEXT, qty REAL, price REAL)""")
    print('create a table: "stocks"')

def addrecords(cur):
  q = "INSERT INTO stocks (date,trans,symbol,qty,price) VALUES (?,?,?,?,?)"
  for i in range(DATA_AMOUNT):
    t = ("20%02d-%02d-%02d" %
          (random.randint(0,10), random.randint(1,12), random.randint(1,31)),
        random.choice(TRANS_TYPE), random.choice(SYMBOL_TYPE),
        random.randint(1, i+1), random.randint(100, 1000000))
    cur.execute(q, t)

def showrecords(cur):
  cur.execute("SELECT * FROM stocks")
  for r in cur:
    print("%s %-5s %-10s %5d %8d" % r)

def main():
  fname = parse_args()
  database = sqlite3.connect(fname)
  cur = database.cursor()
  createtable(cur)
  addrecords(cur)
  showrecords(cur)
  database.commit()
  cur.close()

if __name__ == '__main__':
  main()

# vim: set et ts=2 sw=2 cindent fileencoding=utf-8 :

