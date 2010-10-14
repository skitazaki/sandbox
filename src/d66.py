#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ == """
python %prog {screen_name}

fetches tweets via public timeline.
see also `d30.py`, which scraping normal HTML page.
"""

import datetime
import optparse
import sys

# prior to install using "easy_install" or manually.
import feedparser

def parse_args():
    parser = optparse.OptionParser(__doc__)
    opts, args = parser.parse_args()

    if len(args) != 1:
        parser.error("I can accept only one argument.")

    return args[0]

TWITTER_USER_TIMELINE = "http://api.twitter.com/1/statuses/user_timeline"

def fetch_user_timeline(screen_name):
    url = "%s.atom?screen_name=%s" % (TWITTER_USER_TIMELINE, screen_name)

    feed = feedparser.parse(url)

    for item in feed['items']:
        y,m,d = item['updated_parsed'][:3]
        date = datetime.date(y,m,d)
        print "%s: %s" % (date.strftime("%Y/%m/%d"),
                item['title'].lstrip("%s: " % (screen_name,)))

def main():
    screen_name = parse_args()

    try:
        fetch_user_timeline(screen_name)
    except Exception, e:
        print >>sys.stderr, e
        sys.exit(1)

if __name__ == '__main__':
    main()

# vim: set expandtab tabstop=4 shiftwidth=4 cindent :

