#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple HTTP Server with "twisted.web"
# usage: python d56.py --port 8080

import datetime
import json
import optparse
import os.path
from twisted.web import resource


def parse_args():
    parser = optparse.OptionParser()
    parser.add_option("-p", "--port", dest="port", type="int", default=8080,
            help="port number to listen")
    opts, args = parser.parse_args()
    return opts.port

MIMETYPES = {
  ".html": "text/html",
  ".json": "application/json",
  ".txt": "text/plain",
  ".xml": "text/xml"
}


class SiteHome(resource.Resource):

    def getChild(self, name, request):
        return self

    def render_GET(self, request):
        base, suffix = os.path.splitext(request.path)
        if suffix in MIMETYPES:
            request.setHeader("Content-Type", MIMETYPES[suffix])
        else:
            request.setHeader("Content-Type", "application/octet-stream")
        data = request.args
        n = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        if "date" in data:
            data["date"].append(n)
        else:
            data["date"] = [n]
        print request.path, request.prepath, request.postpath
        if "callback" in data and len(data["callback"]):
            cb = data["callback"][0]
            if cb:
                return "%s(%s);" % (cb, json.dumps(data))
        return json.dumps(data)


def main():
    port = parse_args()
    from twisted.internet import reactor
    from twisted.web import server
    reactor.listenTCP(port, server.Site(SiteHome()))
    try:
        print 'Test server running on %d port...' % port
        reactor.run()
    except KeyboardInterrupt:
        reactor.stop()

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
