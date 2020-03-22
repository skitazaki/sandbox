#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog {keyword}

Fetches tweets via search API using JSON format.
"""

import datetime
import urllib, urllib2

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        raise SystemExit("Use Python 2.6 or higher.")

from sandboxlib import parse_args, ArgumentError

TWITTER_SEARCH = "http://search.twitter.com/search"


def search_tweets(keyword):
    param = {"q": keyword}
    url = "%s.json?%s" % (TWITTER_SEARCH, urllib.urlencode(param))

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
    opts, args = parse_args(doc=__doc__, minargc=1, maxargc=1)
    keyword = args[0]

    search_tweets(keyword)


def test():
    search_tweets("#fctokyo")

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
