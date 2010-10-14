#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """\
usage: python d63.py --port=8080

Simple HTTP Server using `tornado`. The implementation I refered is `here
<http://symfoware.blog68.fc2.com/blog-entry-580.html>`_.
And, this repository contains similar script which uses `BaseHTTPServer` and
`twisted.web`, saved as `d55.py` and `d56.py` respectively.
See also `Tornado official documenation`_.

.. _Tornado official documenation: http://www.tornadoweb.org/documentation
"""

import datetime
import json

import tornado.options
import tornado.web

tornado.options.define(
    "port", default=8080, type=int, help="run on the given port")

class JSONHandler(tornado.web.RequestHandler):

    def get(self, path):
        data = {
            "path":path,
            "request_path":self.request.path,
            "date":datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        }
        self.set_header("Content-Type", "application/json")
        self.write(json.JSONEncoder().encode(data))

def main():

    from tornado.httpserver import HTTPServer
    import tornado.ioloop

    try:
        tornado.options.parse_command_line()
    except tornado.options.Error, e:
        print e
        import sys
        sys.exit(1)
    port = tornado.options.options.port

    http_server = HTTPServer(tornado.web.Application([
        (r"/(.*)", JSONHandler),
    ]))
    try:
        print 'Test server running on %d port...' % port
        http_server.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

# vim: set expandtab tabstop=4 shiftwidth=4 cindent :

