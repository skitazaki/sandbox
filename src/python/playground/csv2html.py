#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options] csv_file

Convert from csv to html list or table.
"""

import csv

from sandboxlib import parse_args, check_file_path, ArgumentError

STYLES = ("list", "table")


def prefook(parser):
    parser.add_option("-s", dest="style",
        help="output style list|table", default="list")


def postfook(opts, args):
    check_file_path(opts, args)
    if not opts.style in STYLES:
        raise ArgumentError('Available styles are "list" or "table".')


class HtmlTuplePrinter:
    """Interface class for "print_html" method.
    """

    def print_header(self):
        pass

    def print_row(self, name, url):
        pass

    def print_footer(self):
        pass


class HtmlListPrinter(HtmlTuplePrinter):

    def print_header(self):
        print "<ul>"

    def print_row(self, name, url):
        print '<li><a href="%s">%s</a></li>' % (url, name)

    def print_footer(self):
        print "</ul>"


class HtmlTablePrinter(HtmlTuplePrinter):

    def print_header(self):
        print "<table><thead><tr><th>Site</th><th>URL</th></tr></thead><tbody>"

    def print_row(self, name, url):
        print '<tr><td>%s</td><td>%s</td></tr>' % (name, url)

    def print_footer(self):
        print "</tbody></table>"

PRINTERS = {"list": HtmlListPrinter, "table": HtmlTablePrinter}
DEFAULT_PRINTER = "list"


def print_html(reader, style=DEFAULT_PRINTER):
    printer = PRINTERS[style]()
    printer.print_header()
    for row in reader:
        if len(row) == 2:
            if row[1].find("http") == 0:
                link = row[1]
            else:
                link = "http://%s" % (row[1])
            printer.print_row(row[0], link)
    printer.print_footer()


def main():
    opts, files = parse_args(doc=__doc__,
                    prefook=prefook, postfook=postfook)
    reader = csv.reader(open(files[0], "r"))
    print_html(reader, style=opts.style)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
