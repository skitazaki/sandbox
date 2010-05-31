#!/usr/bin/env python
# -*- coding: utf-8 -*-
# extract events from iCalendar file.
# example:
# $ python d33.py -f d33.ics -s 2009-01-01 -e 2010-01-1 |sort -r

import datetime
import getopt
import os.path
import sys

try:
  import icalendar
except ImportError:
  print("install \"icalendar\" module with \"easy_install\".")
  sys.exit(1)

def parse_args():
  usage = """usage: python %s -f <iCalendar file> [-s sdate] [-e edate]
Options:
  -f ".ics" file defined by RFC 2445 (mandatory option)
  -s start of the term (default: 1 week ago)
  -e end of the term (default: today)

Note:
  date format must be "YYYY-MM-DD".
  output is not sorted in date order. use "sort" command to clean up.
  """
  try:
    opts, args = getopt.getopt(sys.argv[1:], "f:s:e:")
  except getopt.GetoptError:
    print(usage % (sys.argv[0]))
    sys.exit(1)
  def parse_days(value):
    try:
      y, m, d = [int(e) for e in value.split("-")]
    except ValueError:
      print("[ERROR] invalid format. YYYY-MM-DD is required.")
      sys.exit(1)
    try:
      return datetime.date(y, m, d)
    except ValueError:
      print("[ERROR] invalid date value.")
      sys.exit(1)
  fname = None
  until = datetime.date.today()
  since = until - datetime.timedelta(days=7)
  for o,v in opts:
    if o == "-f":
      fname = v
    elif o == "-s":
      since = parse_days(v)
    elif o == "-e":
      until = parse_days(v)
  if not fname:
    print("[ERROR] \"-f\" option is mandatory.")
    sys.exit(1)
  if not os.path.exists(fname):
    print("[ERROR] \"%s\" not found." % (fname))
    sys.exit(1)
  ical = icalendar.Calendar.from_string(open(fname, "rb").read())
  return (since, until), ical

def main():
  term, ical = parse_args()
  for component in ical.walk():
    if component.name != "VEVENT":
      continue
    date = component.decoded("DTSTART")
    # convert datetime to date type, this conversion also removes the
    # concern whether "tzinfo" is "naive" or "aware".
    if type(date) == datetime.datetime:
      date = date.date()
    if date > term[0] and date <= term[1]:
      print("%s: %s" % (date.strftime("%Y/%m/%d"), component.get("SUMMARY")))

if __name__ == '__main__':
  main()

# vim: set et ts=2 sw=2 cindent fileencoding=utf-8 :

