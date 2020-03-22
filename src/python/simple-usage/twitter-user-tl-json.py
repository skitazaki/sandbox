#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog screen_name [screen_name [ ... ]]

Fetches tweets via public timeline using JSON format.
"""

import datetime
import logging
import urllib, urllib2

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        raise SystemExit("Use Python 2.6 or higher.")

from sandboxlib import parse_args, ArgumentError

TWITTER_USER_TIMELINE = "http://api.twitter.com/1/statuses/user_timeline"


def fetch_user_timeline(screen_name):
    param = {"screen_name": screen_name}
    url = "%s.json?%s" % (TWITTER_USER_TIMELINE, urllib.urlencode(param))

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
    opts, args = parse_args(doc=__doc__, minargc=1)

    for screen_name in args:
        try:
            fetch_user_timeline(screen_name)
        except:
            logging.error("Could not fetch %s's timeline.", screen_name)


def test():
    fetch_user_timeline("kshigeru")

if __name__ == '__main__':
    main()

# vim: set expandtab tabstop=4 shiftwidth=4 cindent :
