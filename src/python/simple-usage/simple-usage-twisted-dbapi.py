#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple usage of Twisted dbapi.

see `Twisted adbapi : asynchronous database access
<http://tonthon.blogspot.com/2011/01/twisted-adbapi-asynchronous-database.html>`_
"""

import logging
import tempfile
import sqlite3

USERS = ((u'yoen', u'Van der Veld', u'Yoen',),
         (u'esteban', u'Garcia Marquez', u'Estebán',),
         (u'mohamed', u'Al Ghâlib', u'Mohamed',),)


def setup_db():
    """ Setup our sqlite database """
    # Tempfile ensure us not to override an existing file
    myfilename = tempfile.mktemp('.sqlite', 'test-bdd', '/tmp')
    conn = sqlite3.connect(myfilename)
    curs = conn.cursor()
    ddl = "Create table users "
    ddl += "(login text unique, name text, forname text)"
    curs.execute(ddl)
    query = "INSERT INTO USERS VALUES (?, ?, ?)"
    for login, name, forname in USERS:
        curs.execute(query, (login, name, forname))
    conn.commit()
    curs.close()
    return myfilename


class Avatar:

    def __init__(self, login, name, forname):
        self.login = login
        self.name = name
        self.forname = forname

    def render(self):
        msg = "Mr '%s %s' is connected under '%s'" % (self.forname,
                                                      self.name,
                                                      self.login,)
        return msg

from twisted.enterprise.adbapi import ConnectionPool

class DBPool:
    """Sqlite connection pool"""

    def __init__(self, dbname):
        self.dbname = dbname
        self.__dbpool = ConnectionPool('sqlite3', self.dbname)

    def shutdown(self):
        """Shutdown function
        It's a required task to shutdown the database connection pool:
        garbage collector doesn't shutdown associated thread"""
        self.__dbpool.close()

    def build_avatar(self, dbentries):
        """Build avatar from dbentries"""
        login, name, forname = dbentries[0]
        return Avatar(login, name, forname)

    def get_user_avatar(self, login):
        """Build associated avatar object"""
        query = 'SELECT * from `users` where login=?'
        return self.__dbpool.runQuery(query, (login,)).addCallback(self.build_avatar)


def main():

    def printResult(result):
        for r in result:
            print(r[1])

    from twisted.internet.defer import DeferredList
    from twisted.internet import reactor

    # We initialize the db pool with our dbname retrieved in the first step.
    dbname = setup_db()
    dbpool = DBPool(dbname)
    # DeferredList seems more adapted than chained callbacks in this sort of cases
    ret_render = lambda avatar: avatar.render()
    deferreds = [dbpool.get_user_avatar(login).addCallback(ret_render)
                            for login in ('yoen', 'esteban', 'mohamed',)]

    dlist = DeferredList(deferreds)
    dlist.addCallback(printResult)
    # We ask our pool to shutdown all the initialized connections
    dlist.addCallback(lambda _:dbpool.shutdown)
    # Want to get the hand back :-)
    reactor.callLater(4, reactor.stop)
    reactor.run()

if __name__ == "__main__":
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
