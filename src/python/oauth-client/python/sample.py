#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""\\
Test script to run sample client implementation.

:Author: KITAZAKI Shigeru
:Version: 0.4
"""

import logging
import os.path
import ConfigParser

# local modules.
import models
from util import parse_args, load_object
from oauth_wrap import create as create_client

DEFAULT_SETTING_FILE = 'settings.ini'

SERVICE = {
    'cybozulive': 'cybozulive.Api',
    'twitter': 'twitter_wrap.Api'
}

SERVICE_SAMPLES = {
    'cybozulive': 'cybozulive.run_sample',
    'twitter': 'twitter_wrap.run_sample'
}


def main():
    opts, args = parse_args()
    fname = opts.filename or DEFAULT_SETTING_FILE
    if not os.path.exists(fname):
        raise SystemExit("%s is not found." % (fname,))
    parser = ConfigParser.SafeConfigParser()
    if not parser.read(fname):
        raise SystemExit("%s has no section." % (fname,))
    if not args:
        raise SystemExit("No target was given.")
    target = args[0]
    try:
        ck = parser.get(target, 'consumer_key')
        secret = parser.get(target, 'consumer_secret')
        if not (ck and secret):
            msg = ("No consumer token was found.",
                   "Check 'consumer_key' and 'consumer_secret' on %s." % (
                       target))
            raise SystemExit('\n'.join(msg))
    except ConfigParser.NoOptionError, e:
        raise SystemExit(e.message)
    consumer_token = (ck, secret)

    sample_user = 'TEST_USER'
    API = load_object(SERVICE[target])
    ret = models.find(models.AccessToken,
            service_provider_name=target,
            user_name=sample_user)
    if ret:
        access_token = (ret.oauth_token_key, ret.oauth_token_secret)
        client = create_client(consumer_token, access_token)
        api = API(client)
        if target in SERVICE_SAMPLES:
            run = load_object(SERVICE_SAMPLES[target])
            run(api)
        else:
            logging.warn("No sample was found for %s." % (target,))
    else:
        client = create_client(consumer_token)
        api = API(client)
        access_token = api.initialize()
        if access_token:
            assert len(access_token) == 2
            token = models.AccessToken(service_provider_name=target,
                    user_name=sample_user,
                    oauth_token_key=access_token[0],
                    oauth_token_secret=access_token[1])
            token.put()

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
