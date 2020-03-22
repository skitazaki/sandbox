#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options] file [,file...]

Sample usage of MySQLdb whose settings is provided by JSON file.
"""

import logging

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        raise SystemExit("json module is not found on your system.")
try:
    import MySQLdb
except ImportError:
    raise SystemExit("`MySQLdb` module is not found on your system.")

from sandboxlib import parse_args, check_file_path


def main():
    opts, files = parse_args(doc=__doc__, postfook=check_file_path)

    def get_database_info(info):
        host = info["host"] or "127.0.0.1"
        port = info["port"] or 3306
        database = info["database"] or "test"
        username = info["username"] or ""
        password = info["password"] or ""
        return host, port, database, username, password

    def process(database):
        cur = database.cursor()
        d61.createtable(cur)
        d61.addrecords(cur)
        d61.showrecords(cur)
        database.commit()
        cur.close()

    for fname in files:
        logging.info("start to process: %s", fname)
        try:
            info = json.load(open(fname))
        except:
            logging.error("%s is invalid JSON format.", fname)
            continue

        host, port, database, username, password = get_database_info(info)
        logging.debug("connect \"%s\" of %s@%s:%d" %
                (database, username, host, port))
        try:
            conn = MySQLdb.connect(
                        host=host, port=port,
                        db=database,
                        user=username, passwd=password)
        except Exception, e:
            logging.error("could not connect MySQL. %s" % (e,))
            continue

        process(conn)

if __name__ == "__main__":
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
