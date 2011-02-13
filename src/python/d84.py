#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ == """
python %prog {screen_name}

Fetches tweets via public timeline using JSON format.
see also `d66.py`, which uses Atom data.
"""

import datetime
import logging
import optparse
import sys
import urllib2

try:
    import simplejson as json
except ImportError:
    import json

TWITTER_USER_TIMELINE = "http://api.twitter.com/1/statuses/user_timeline"


def parse_args():
    parser = optparse.OptionParser(__doc__)
    opts, args = parser.parse_args()

    if len(args) != 1:
        parser.error("I can accept only one argument.")

    return args[0]


def fetch_user_timeline(screen_name):
    url = "%s.json?screen_name=%s" % (TWITTER_USER_TIMELINE, screen_name)

    ret = urllib2.urlopen(url)
    if ret.code != 200:
        raise Error(ret.read())
    tweets = json.load(ret)

    for tweet in tweets:
        t = datetime.datetime.strptime(tweet.get("created_at"),
              "%a %b %d %H:%M:%S +0000 %Y")
        assert str(tweet.get("id")) == tweet.get("id_str")
        print "%s: %s" % (t.strftime("%Y/%m/%d"), tweet.get("text"))


def main():
    screen_name = parse_args()

    try:
        fetch_user_timeline(screen_name)
    except Exception, e:
        logging.error(e)
        sys.exit(1)


def test():
    fetch_user_timeline("kshigeru")

if __name__ == '__main__':
    main()

# vim: set expandtab tabstop=4 shiftwidth=4 cindent :
