#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Shows list of document on Google Spreadsheet.
# <http://code.google.com/intl/ja/apis/spreadsheets/data/1.0/developers_guide_python.html>
# example:
# python d29.py -u skitazaki

import getpass
import gdata.spreadsheet.service

client = gdata.spreadsheet.service.SpreadsheetsService()
user = getpass.getuser()


def usage(program):
    print '''usage: python %s [-u user]
    -u user name (default:%s)
    ''' % (program, user)


def gdatalogin():
    client.email = user
    print("attempt to login as %s to %s" % (user, client.service))
    client.password = getpass.getpass()
    client.ProgrammaticLogin()


def get_spreadsheets():
    spreadsheets = client.GetSpreadsheetsFeed()
    for i, entry in enumerate(spreadsheets.entry):
        print("%3d,%s\n\t%s" % (i, entry.title.text, entry.id.text))


def main():
    gdatalogin()
    get_spreadsheets()

if __name__ == '__main__':
    import getopt
    import sys
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:")
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(1)
    for o, v in opts:
        if o == "-u":
            user = v
        else:
            pass
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
