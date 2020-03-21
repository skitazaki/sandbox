#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Sample storage implementation for access token of OAuth with `sqlite3`.
#
# TODO: write test cases.
# TODO: define model meta class.
#

import atexit
import logging
import sqlite3

from util import load_object

DEFAULT_SQLITE_FILE = '.oauth-client.sqlite'


class Database(object):

    obj = None

    @staticmethod
    def cursor():
        if not Database.obj:
            Database.obj = load()
        return Database.obj.cursor()

    @staticmethod
    def terminate():
        """Close internal database after commit."""
        logging.debug("terminate program after commit database.")
        if Database.obj:
           Database.obj.commit()

atexit.register(Database.terminate)

def find(cls, **kwargs):
    '''Finds models.

    Args:
    :param class cls: class of model.
    :param dict kwargs: filter condition for WHERE statement.
    :rtype: model instances if found, otherwise None.
    '''
    fields = cls.fields()
    table = cls.table()
    cur = Database.cursor()
    sql = "SELECT `" + '`,`'.join([f for f in fields])
    sql += "` FROM " + table
    if kwargs:
        filter = ' AND '.join(["`%s` = '%s'" % t for t in kwargs.iteritems()])
        sql += " WHERE " + filter
    logging.debug("SQL: %s" % (sql,))
    cur.execute(sql)
    r = cur.fetchone()
    cur.close()
    if r:
        m = cls()
        n = 0
        for f in fields:
            object.__setattr__(m, f, r[n])
            n += 1
        return m
    else:
        return None


class ModelMeta(type):

    def __getattribute__(*args):
        cls, method = args
        if method == 'fields':
            def get_fields():
                fields = []
                for f in dir(cls):
                    if not f.startswith('_') and not callable(getattr(cls, f)):
                        fields.append(f)
                return fields
            return get_fields
        elif method == 'table':
            def get_table():
                return cls.__name__.lower()
            return get_table
        else:
            return type.__getattribute__(*args)


class Model(object):

    __metaclass__ = ModelMeta

    def __init__(self, **kwargs):
        fields = type(self).fields()

        for k, v in kwargs.iteritems():
            if k in fields:
                object.__setattr__(self, k, v)

    def put(self):
        '''Save model instance.'''
        cur = Database.cursor()
        fields = type(self).fields()
        keys = []
        values = []
        for f in fields:
            v = getattr(self, f)
            if v:
                keys.append(f)
                values.append(v)
        # TODO: use prepared statement, and use pickle for complex data.
        table = type(self).table()
        sql = "INSERT INTO " + table + ' ('
        sql += ','.join([f for f in keys])
        sql += ') VALUES ('
        sql += ','.join(["'%s'" % (v,) for v in values])
        sql += ')'
        logging.debug(sql)
        # TODO: update when service provider and user name are duplicate.
        cur.execute(sql)
        cur.close()


def create_sql(cls):
    table = cls.table()
    fields = cls.fields()

    sql = 'CREATE TABLE `' + table + '` ('
    # TODO enable to set various field types.
    sql += ','.join(['`%s` TEXT' % (f, ) for f in fields])
    sql += ')'
    return sql


class AccessToken(Model):

    service_provider_name = None
    user_name = None
    oauth_token_key = None
    oauth_token_secret = None


def load(fname=None):
    """Constructs database with `sqlite3`."""
    dbname = fname or DEFAULT_SQLITE_FILE
    database = sqlite3.connect(dbname)

    cur = database.cursor()

    def initialize(cls_name):
        """Initialize data store.
        """
        cls = load_object(cls_name)
        tbl = cls.table()
        cur.execute("""SELECT sql FROM sqlite_master
          WHERE type='table' AND tbl_name='%s'""" % (tbl,))
        r = cur.fetchone()
        if r:
            logging.debug('"%s" is already created: %s' % (tbl, r))
        else:
        # it's okay to use "IF NOT EXISTS", but checking current status is more
        # user-friendly to avoid to overwrite current data.
            sql = create_sql(cls)
            cur.execute(sql)
            logging.debug('create a table: "%s"' % (tbl,))

    initialize('models.AccessToken')
    # TODO separate into each module or use `dir()`.
    initialize('cybozulive.Notification')
    initialize('cybozulive.Task')
    initialize('cybozulive.Schedule')
    initialize('cybozulive.Group')
    initialize('cybozulive.Comment')
    initialize('cybozulive.Board')
    cur.close()
    return database


def test():
    Database.obj = load('.oauth-client-test.sqlite')
    target = 'localhost'
    access_token = ('SAMPLE', 'SAMPLE')
    token = AccessToken(service_provider_name=target,
            user_name='TEST_USER',
            oauth_token_key=access_token[0],
            oauth_token_secret=access_token[1])
    token.put()
    access_token = find(AccessToken, service_provider_name=target)
    assert access_token
    assert access_token.oauth_token_key
    assert access_token.oauth_token_secret

if __name__ == '__main__':
    test()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
