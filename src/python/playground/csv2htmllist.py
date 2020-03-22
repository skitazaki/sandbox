#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options] csv_file

Convert from csv to html list or json.
"""

import csv

from sandboxlib import parse_args, check_file_path, ArgumentError


def prefook(parser):
    parser.add_option("-t", dest="outtype",
        help="output type html|json", default="html")


def postfook(opts, args):
    check_file_path(opts, args)
    if not opts.outtype in ("html", "json"):
        raise ArgumentError('Available types are "html" or "json".')


def print_html(reader):
    print "<ul>"
    for row in reader:
        if len(row) == 2:
            if row[1].find("http") == 0:
                link = row[1]
            else:
                link = "http://%s" % (row[1])
            print '<li><a href="%s">%s</a></li>' % (link, row[0])
    print "</ul>"


def print_json(reader):
    try:
        import json
    except ImportError:
        raise SystemExit("Use Python 2.6 or higher.")
    data = [{"item":r[0], "href":r[1]} for r in reader if len(r) == 2]
    print json.dumps(data, indent=2)


def main():
    opts, files = parse_args(doc=__doc__,
                    prefook=prefook, postfook=postfook)
    handler = {"html": print_html, "json": print_json}
    reader = csv.reader(open(files[0], "r"))
    handler[opts.outtype](reader)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
