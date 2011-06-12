#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """\
python %prog [option] file [,file...]

Sample usage of MySQLdb whose settings is provided by JSON file.
The real procedures are implemented in `d61.py`, so your PATHONPATH must
include this directory. The easiest way is to change directory to here:D
"""

import logging
import optparse
import os.path
import sys

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        print("json module is not found on your system.")
        sys.exit(1)

try:
    import MySQLdb
except ImportError:
    print("Install \"MySQLdb\" at first.")
    sys.exit(1)


def parse_args():
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-v", "--verbose", dest="verbose",
            default=False, action="store_true", help="verbose mode")

    opts, args = parser.parse_args()

    if not args:
        parser.error("no setting file is specified.")

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)

    return args


def main():
    files = parse_args()

    def get_database_info(info):
        host = info["host"] or "127.0.0.1"
        port = info["port"] or 3306
        database = info["database"] or "test"
        username = info["username"] or ""
        password = info["password"] or ""
        return host, port, database, username, password

    import d61

    def process(database):
        cur = database.cursor()
        d61.createtable(cur)
        d61.addrecords(cur)
        d61.showrecords(cur)
        database.commit()
        cur.close()

    for file in files:
        # Check file exists and valid JSON format
        if not os.path.exists(file):
            logging.error("%s is not found." % (file,))
            continue
        try:
            info = json.load(open(file))
        except:
            logging.error("%s is invalid JSON file format." % (file,))
            continue

        logging.info("start to process: %s" % (file))
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
