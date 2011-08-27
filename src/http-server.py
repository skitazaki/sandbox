#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple HTTP Server to serve sandbox contents.
"""

#import anyjson as json
import json
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


MIMETYPES = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.json': 'application/json',
  '.jsonp': 'application/javascript',
  '.css': 'text/css',
  '.txt': 'text/plain',
  '.xml': 'application/xml',
  '.png': 'image/png',
  '.atom': 'application/atom+xml',
}

BASEDIR = os.path.abspath(os.path.join(__file__, '..', '..'))
LIBDIR = os.path.join(BASEDIR, 'lib')
CONTENTSDIR = os.path.join(BASEDIR, 'src', 'javascript')

class RequestHandler(BaseHTTPRequestHandler):

    jQuery = os.path.join(LIBDIR, 'jquery.min.js')
    jQueryUI = os.path.join(LIBDIR, 'jquery-ui.min.js')
    jQueryTmpl = os.path.join(LIBDIR, 'jquery.tmpl.min.js')
    jQueryHistory = os.path.join(LIBDIR, 'jquery.history.min.js')
    DataJS = os.path.join(LIBDIR, 'datajs.min.js')
    RaphaelJS = os.path.join(LIBDIR, 'raphael.min.js')

    def _send_file(self, fname):
        _, suffix = os.path.splitext(fname)
        self.send_response(200)
        if suffix in MIMETYPES:
            self.send_header('Content-Type', MIMETYPES[suffix])
        else:
            self.send_header('Content-Type', 'application/octet-stream')
        self.end_headers()
        self.wfile.write(open(fname).read())

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write('<ul>')
            for f in os.listdir(CONTENTSDIR):
                if f.endswith('.html'):
                    self.wfile.write('<li><a href="%s">%s</a></li>' % (f, f))
                elif f.endswith('~') or f.startswith('.'):
                    continue
                else:
                    self.wfile.write('<li>%s</li>' % (f,))
            self.wfile.write('</ul>')
            return

        js = None
        if self.path.startswith('/static/jquery.min.js'):
            js = self.jQuery
        elif self.path.startswith('/static/jquery-ui.min.js'):
            js = self.jQueryUI
        elif self.path.startswith('/static/jquery.tmpl.min.js'):
            js = self.jQueryTmpl
        elif self.path.startswith('/static/jquery.history.min.js'):
            js = self.jQueryHistory
        elif self.path.startswith('/static/datajs.min.js'):
            js = self.DataJS
        elif self.path.startswith('/static/raphael.min.js'):
            js = self.RaphaelJS
        if js:
            self._send_file(js)
            return

        pos = self.path.find('?')
        if pos > 0 and len(self.path) > pos + 1:
            path, query = self.path[:pos], self.path[pos + 1:]
        else:
            path, query = self.path, None

        c = os.path.join(CONTENTSDIR, path[1:])
        if os.path.isfile(c):
            self._send_file(c)
            return
        c = os.path.join(LIBDIR, path[1:])
        if os.path.isfile(c):
            self._send_file(c)
            return
        # handle JSONP call.
        callback = None
        data = {}
        if query:
            for t in query.split('&'):
                _ = t.split('=')
                if len(_) == 1:
                    k, v = t, None
                elif len(_) == 2:
                    k, v = _
                else:
                    # Invalid query.
                    continue
                if k == 'callback':
                    callback = v
                else:
                    data[k] = v
        if callback:
            self.send_response(200)
            self.send_header('Content-Type', MIMETYPES['.jsonp'])
            self.end_headers()
            self.wfile.write(callback + "(")
            self.wfile.write(json.dumps(data))
            self.wfile.write(");")
            return
        self.send_error(404, "File not found: %s" % self.path)


def main():
    import sys
    port = int(sys.argv[1]) if len(sys.argv) == 2 else 8000
    try:
        server = HTTPServer(('', port), RequestHandler)
        print 'Test server running on %d port...' % port
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
