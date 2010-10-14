#!/usr/bin/env python
# -*- coding: utf-8 -*-
# fetches one-week tweets via public RSS feed.

import datetime
import httplib
import re
import sys

# prior to install using "easy_install" or manually.
import feedparser

def usage(program):
  print('''usage: python %s tid [tid ...]''' % (program))

httpconnection = httplib.HTTPConnection("twitter.com")
# for scraping to get the link of RSS feed with sequencial ID.
feedlink = re.compile('statuses/user_timeline/(\d+).rss')
beginning = datetime.date.today() - datetime.timedelta(days=7)

def gettwitterfeed(tid):
  httpconnection.request("GET", "/%s" % tid)
  res = httpconnection.getresponse()
  if res.status >= 400:
    raise IOError("not found '%s'" % tid)
  for l in res.read().split():
    m = feedlink.search(l)
    if m:
      return feedparser.parse("http://twitter.com/%s" % m.group())

def showtweets(tid):
  try:
    feed = gettwitterfeed(tid)
  except IOError:
    print("could not find: %s" % tid)
  if feed:
    print("= %s" % tid)
    for item in feed['items']:
      y,m,d = item['updated_parsed'][:3]
      if beginning < datetime.date(y,m,d):
        print item['summary'].lstrip("%s: " % tid)

if __name__ == '__main__':
  if len(sys.argv) == 1:
    usage(sys.argv[0])
    sys.exit(1)
  else:
    [showtweets(tid) for tid in sys.argv[1:]]
    httpconnection.close()

# vim: set et ts=2 sw=2 cindent fileencoding=utf-8 :

