#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Login with GData Client API, and shows current token.
# <http://code.google.com/intl/ja/apis/gdata/docs/auth/clientlogin.html>
# example:
# python d24.py -u skitazaki -s blogger

import getpass
import gdata.service

user = getpass.getuser()
client = gdata.service.GDataService()


def usage(program):
    print '''usage: python %s [-u user] [-s service]
    -u user name (default:%s)
    -s service name (default:blogger)
    ''' % (program, user)


def gdatalogin():
    client.email = user
    print("attempt to login as %s to %s" % (user, client.service))
    client.password = getpass.getpass()
    client.ProgrammaticLogin()


def main(which):
    client.service = which
    gdatalogin()
    print(client.current_token)

if __name__ == '__main__':
    import getopt
    import sys
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:s:")
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(1)
    which = "blogger"
    for o, v in opts:
        if o == "-u":
            user = v
        elif o == "-s":
            which = v
        else:
            pass
    main(which)

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
