#!/usr/bin/env python
# -*- coding: utf-8 -*-
# convert from csv to html list or json
# $ python d32.py -t html d32.csv

import csv
import getopt
import json
import sys

def parse_args():
  usage = """usage: python %s -t html|json csv-file-name
  """
  try:
    opts, args = getopt.getopt(sys.argv[1:], "t:")
  except getopt.GetoptError:
    print usage % (sys.argv[0])
    sys.exit(1)
  format = None
  for o,v in opts:
    if o == "-t":
      format = v
  if not format:
    print 'specify "-t" option'
    sys.exit(1)
  if not format in ("html", "json"):
    print 'available formats are "html" or "json"'
    sys.exit(1)
  if len(args) != 1:
    print 'invalid argument count: %d' % (len(args))
    sys.exit(1)
  fname = args[0]
  try:
    return (format, csv.reader(open(fname, "r")))
  except IOError:
    print 'invalid file name: %s' % (fname)
    sys.exit(1)

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
  data = [{"item":r[0], "href":r[1]} for r in reader if len(r) == 2]
  print json.dumps(data, indent=2)

def main():
  handler = {"html":print_html, "json":print_json}
  format, reader = parse_args()
  handler[format](reader)

if __name__ == '__main__':
  main()

# vim: set et ts=2 sw=2 cindent fileencoding=utf-8 :

