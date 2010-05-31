#!/usr/bin/env python
# -*- coding: utf-8 -*-
# convert iCalendar file into hCalendar.
# example:
# $ python d38.py -f d33.ics -s 2010-01-01 >test.html &&
#     xmllint --html --valid test.html && rm test.html
# note:
# (http://microformats.org/wiki/hcalendar)

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
  output is not sorted in date order.
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
  if since > until:
    print("[ERROR] term is invalid. begin:%s, end:%s" %
        (since.strftime("%Y-%m-%d"), until.strftime("%Y-%m-%d")))
    sys.exit(1)
  ical = icalendar.Calendar.from_string(open(fname, "rb").read())
  return (since, until), ical

def printevent(event):
  print("""<div class="vevent">""")
  if "summary" in event:
    print("""<h3 class="summary">%s</h3>""" % (event.get("summary")))
  if "url" in event:
    e = event.get("url")
    print("""<a class="url" href="%s">%s</a>""" % (e, e))
  if "dtstart" in event:
    d = event.decoded("dtstart")
    print("""<abbr class="dtstart" title="%s">%s</abbr>""" %
        (d.strftime("%Y%m%dT%X"), d.strftime("%a, %d. %b %Y")))
  if "dtend" in event:
    d = event.decoded("dtend")
    print(""" - <abbr class="dtend" title="%s">%s</abbr>""" %
        (d.strftime("%Y%m%dT%X"), d.strftime("%a, %d. %b")))
  if "description" in event:
    t = event.get("description").strip()
    if t:
      print("""<p class="description">%s</p>""" % (t))
  print("</div>")

def calendarconv(term, ical):
  for component in ical.walk():
    if component.name != "VEVENT":
      continue
    date = component.decoded("DTSTART")
    # convert datetime to date type, this conversion also removes the
    # concern whether "tzinfo" is "naive" or "aware".
    if type(date) == datetime.datetime:
      date = date.date()
    if date > term[0] and date <= term[1]:
      printevent(component)

def main():
  term, ical = parse_args()
  print("""<html><head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <meta http-equiv="content-script-type" content="text/javascript" />
  <meta http-equiv="content-style-type" content="text/css" />
  <title>hCalendar from .ics file</title>
  <link rel="profile" href="http://microformats.org/profile/hcalendar" />
  </head><body>""")
  calendarconv(term, ical)
  print("</body></html>")

if __name__ == '__main__':
  main()

# vim: set et ts=2 sw=2 cindent fileencoding=utf-8 :

