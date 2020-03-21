#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""\\
Wrapper script of `twitter` module.

:Author: KITAZAKI Shigeru
:Version: 0.1
"""

import logging

from twitter import Twitter
from twitter.oauth import OAuth
from twitter.oauth_dance import oauth_dance
from twitter.api import TwitterHTTPError

APPLICATION_NAME = 'MyApp'


class Api(object):

    def __init__(self, client):
        self.client = client

    def accessor(self):
        if self.client.token is None:
            raise Error("Client is not initialized.")
        c, a = self.client.consumer, self.client.token
        oauth = OAuth(a.key, a.secret, c.key, c.secret)
        return Twitter(auth=oauth)


    def initialize(self):
        c = self.client.consumer
        try:
            ret = oauth_dance(APPLICATION_NAME, c.key, c.secret)
            return ret
        except TwitterHTTPError, e:
            logging.error(e)


def run_sample(api):
    import sys
    writer = sys.stdout

    def printer(item):
        print >>writer, '-' * 79
        print >>writer, "[%s] %s at %s (%s)" % (item['user']['screen_name'],
                item['user']['name'], item['created_at'], item['id_str'])
        print >>writer, item['text']

    accessor = api.accessor()

    for tl in accessor.statuses.public_timeline():
        printer(tl)

    for tl in accessor.statuses.user_timeline():
        printer(tl)

    for tl in accessor.statuses.home_timeline():
        printer(tl)

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
