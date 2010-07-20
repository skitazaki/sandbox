#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple HTTP Server
# usage: python d55.py --port 8080

import datetime
import json
import optparse
import os.path
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

def parse_args():
  parser = optparse.OptionParser()
  parser.add_option("-p", "--port", dest="port", type="int", default=8080,
          help="port number to listen")
  opts, args = parser.parse_args()
  return opts.port

MIMETYPES = {
  ".html":"text/html",
  ".json":"application/json",
  ".txt": "text/plain",
  ".xml": "text/xml"
}

class RequestHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    try:
      _ = self.path.split("?")
      if len(_) == 1:
        path = _[0]
        query = None
      elif len(_) == 2:
        path, query = _
      else:
        raise IOError()
      base, suffix = os.path.splitext(path)
      self.send_response(200)
      if suffix in MIMETYPES:
        self.send_header("Content-Type", MIMETYPES[suffix])
      else:
        self.send_header("Content-Type", "application/octet-stream")
      self.end_headers()
      data = {"path":path,
        "date":datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")}
      callback = None
      if query:
        for t in query.split("&"):
          _ = t.split("=")
          if len(_) == 1:
            k = _[0]
            v = None
          elif len(_) == 2:
            k, v = _
          else:
            print "Invalid query: %s" % t
            continue
          if k == "callback":
            callback = v
          else:
            data[k] = v
      if callback:
        self.wfile.write(callback + "(")
      self.wfile.write(json.dumps(data))
      if callback:
        self.wfile.write(");")
    except IOError:
      self.send_error(404, "File not found: %s" % self.path)

def main():
  port = parse_args()
  try:
    server = HTTPServer(('', port), RequestHandler)
    print 'Test server running on %d port...' % port
    server.serve_forever()
  except KeyboardInterrupt:
    server.socket.close()

if __name__ == '__main__':
  main()

# vim: set expandtab tabstop=2 shiftwidth=2 cindent :

