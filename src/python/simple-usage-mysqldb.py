#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options]

Sample usage of MySQLdb.
"""

import random
try:
    import MySQLdb
except ImportError:
    raise SystemExit("`MySQLdb` module is not found on your system.")

# NOTE: set this value from command line argument.
DATA_AMOUNT = 50

# enumeration for generating sample data
TRANS_TYPE = ("BUY", "SELL")
SYMBOL_TYPE = ("Apple", "Google", "Microsoft", "Sony")


def createtable(cur):
    cur.execute("""SHOW tables like 'stocks'""")
    r = cur.fetchone()
    if r:
        print('"stocks" is already created: %s' % r)
    else:
        # it's okay to use "IF NOT EXISTS", but checking current status is more
        # user-friendly to avoid to overwrite current data.
        cur.execute("""CREATE TABLE stocks (
          date DATE, trans VARCHAR(5), symbol VARCHAR(10),
          qty REAL, price REAL)""")
        print('create a table: "stocks"')


def addrecords(cur):
    q = "INSERT INTO stocks (date,trans,symbol,qty,price)"
    q += " VALUES (%s,%s,%s,%s,%s)"
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
        print("%s %-5s %-10s %5s %8s" % r)


def main():
    database = MySQLdb.connect(db="test")
    cur = database.cursor()
    createtable(cur)
    addrecords(cur)
    showrecords(cur)
    database.commit()
    cur.close()

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
