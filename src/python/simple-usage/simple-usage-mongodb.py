#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""\
Try MongoDB with `pymongo`.

`Tutorial PyMongo v1.9+ <http://api.mongodb.org/python/1.9%2B/tutorial.html>`_
is a good starting point, and this works as well on Windows.
The installation is ::

    $ sudo easy_install pymongo

After running server daemon, try it out ::

    $ python simple-usage-mongodb.py

or ::

    $ nosetests simple-usage-mongodb.py
"""

from pymongo import Connection


def test_insert_and_find():
    con = Connection()
    con.db.test.insert({"key": "abc"})
    ret = con.db.test.find_one()
    print ret
    assert ret["_id"]
    assert ret["key"]

if __name__ == '__main__':
    test_insert_and_find()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
