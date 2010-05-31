#!/usr/bin/env python
# -*- coding: utf-8 -*-
# convert from csv to html list or table
# $ python d36.py -s table d32.csv

import csv
import getopt
import sys

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

PRINTERS = {"list":HtmlListPrinter, "table":HtmlTablePrinter}
DEFAULT_PRINTER = "list"

def parse_args():
  usage = """usage: python %s [-s style] csv-file-name
Options:
  -s  style either of "list" or "table" (default:list)
  """
  try:
    opts, args = getopt.getopt(sys.argv[1:], "s:")
  except getopt.GetoptError:
    print usage % (sys.argv[0])
    sys.exit(1)
  style = None
  for o,v in opts:
    if o == "-s":
      style = v
  if len(args) != 1:
    print 'invalid argument count: %d' % (len(args))
    sys.exit(1)
  fname = args[0]
  try:
    return (style, csv.reader(open(fname, "r")))
  except IOError:
    print 'invalid file name: %s' % (fname)
    sys.exit(1)

def print_html(reader, **kwargs):
  style = kwargs.get("style", None) or DEFAULT_PRINTER
  if style in PRINTERS:
    printer = PRINTERS[style]()
  else:
    raise IOError("invalid printer style: %s" % (style))
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
  style, reader = parse_args()
  print_html(reader, style=style)

if __name__ == '__main__':
  main()

# vim: set et ts=2 sw=2 cindent fileencoding=utf-8 :
