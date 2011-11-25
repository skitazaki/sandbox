#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options]

Sample usage of sqlite.
* <http://docs.python.org/library/sqlite3.html>
* <http://net-newbie.com/sqlite/sqlite.html>
"""

import logging
import random
try:
    import sqlite3
except ImportError:
    raise SystemExit("Python 2.5 or higher required.")

from sandboxlib import parse_args

# NOTE: set this value from command line argument.
DATA_AMOUNT = 50

# enumeration for generating sample data
TRANS_TYPE = ("BUY", "SELL")
SYMBOL_TYPE = ("Apple", "Google", "Microsoft", "Sony")


def createtable(cur):
    cur.execute("""SELECT sql FROM sqlite_master
        WHERE type='table' AND tbl_name='stocks'""")
    r = cur.fetchone()
    if r:
        loggng.info('"stocks" is already created: %s', r)
    else:
        # it's okay to use "IF NOT EXISTS", but checking current status is more
        # user-friendly to avoid to overwrite current data.
        cur.execute("""CREATE TABLE stocks (
          date TEXT, trans TEXT, symbol TEXT, qty REAL, price REAL)""")
        logging.info('create a table: "stocks"')


def addrecords(cur):
    q = "INSERT INTO stocks (date,trans,symbol,qty,price) VALUES (?,?,?,?,?)"
    for i in range(DATA_AMOUNT):
        t = ("20%02d-%02d-%02d" %
              (random.randint(0, 10), random.randint(1, 12),
               random.randint(1, 31)),
            random.choice(TRANS_TYPE), random.choice(SYMBOL_TYPE),
            random.randint(1, i + 1), random.randint(100, 1000000))
        cur.execute(q, t)


def showrecords(cur):
    cur.execute("SELECT * FROM stocks")
    for r in cur:
        print("%s %-5s %-10s %5d %8d" % r)


def main():
    opts, _ = parse_args(doc=__doc__, maxargc=0)
    fname = opts.output or ':memory:'
    database = sqlite3.connect(fname)
    cur = database.cursor()
    createtable(cur)
    addrecords(cur)
    showrecords(cur)
    database.commit()
    cur.close()

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
