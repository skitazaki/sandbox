#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Try using "zope.interface".
# usage:
# $ python d52.py
# note:
# http://svn.zope.org/zope.interface/trunk/src/zope/interface/README.txt?view=markup

from zope.interface import Interface, Attribute
from zope.interface import implements


class IAction(Interface):
    """Simple interface for user action such as web application.
    This class will be exported for beautiful documentation.
    """

    service = Attribute("some nice service")

    def get(request, response):
        """Action for GET request
        @param request: HTTP request object
        @param response: HTTP response object
        @return: None
        """


class SimpleAction(object):
    implements(IAction)

    def get(self, request, response):
        response.out.write("request: %s\n" % request)


class Request(object):

    def __str__(self):
        return "this is a request object!"

import sys


class Response(object):
    out = sys.stdout


def main():
    print "IAction: %s" % IAction.__doc__
    print "`get` %s\n%s" % (
        IAction["get"].getSignatureString(), IAction["get"].__doc__)
    action = SimpleAction()
    req = Request()
    res = Response()
    action.get(req, res)
    print action.get

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
