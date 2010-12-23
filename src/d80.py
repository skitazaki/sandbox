#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample script to use WSGI on Twisted.

This script is based on `Twisted Web in 60 seconds: WSGI
<http://jcalderone.livejournal.com/51888.html>`_.

Just try it after installing Twisted. ::

    $ twistd -n web -p 8888 --wsgi d80.application

You can see the response with `wget` utility. ::

    $ wget -qSO - http://localhost:8888/a.txt
"""

import os.path

from twisted.web.wsgi import WSGIResource
from twisted.internet import reactor

MIMETYPES = {
  ".html":"text/html",
  ".json":"application/json",
  ".txt": "text/plain",
  ".xml": "text/xml"
}

def application(environ, start_response):
    query = environ["QUERY_STRING"]
    (name, ext) = os.path.splitext(environ["PATH_INFO"])
    if ext in MIMETYPES:
        ct = MIMETYPES[ext]
    else:
        ct = "application/octet-stream"
    start_response("200 OK", [("Content-type", ct)])
    return ["Hello, world!", name, query]

resource = WSGIResource(reactor, reactor.getThreadPool(), application)

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :

