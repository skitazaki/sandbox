#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ == """\
python %prog {hashtag-name-except-hash}

Fetches tweets via search API using JSON format.
see also `d84.py`, which uses user timeline.
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

TWITTER_SEARCH = "http://search.twitter.com/search.json"


def parse_args():
    parser = optparse.OptionParser(__doc__)
    opts, args = parser.parse_args()

    if len(args) != 1:
        parser.error("I can accept only one argument.")

    return args[0]


def fetch_channel(channel):
    url = "%s?q=%%23%s" % (TWITTER_SEARCH, channel)

    ret = urllib2.urlopen(url)
    if ret.code != 200:
        raise Error(ret.read())
    tweets = json.load(ret)

    print "--- Meta information ---"
    print "Current:", tweets.get("refresh_url")
    print "Max ID:", tweets.get("max_id_str")
    print "Next Page:", tweets.get("next_page")
    print "-" * 78

    for tweet in tweets["results"]:
        t = datetime.datetime.strptime(tweet.get("created_at"),
              "%a, %d %b %Y %H:%M:%S +0000")
        assert str(tweet.get("id")) == tweet.get("id_str")
        print "%s: %s [%s]" % (
                t.strftime("%Y/%m/%d %H:%M"),
                tweet.get("text"), tweet.get("from_user"))


def main():
    channel = parse_args()

    try:
        fetch_channel(channel)
    except Exception, e:
        logging.error(e)
        sys.exit(1)


def test():
    fetch_channel("fctokyo")

if __name__ == '__main__':
    main()

# vim: set expandtab tabstop=4 shiftwidth=4 cindent :
