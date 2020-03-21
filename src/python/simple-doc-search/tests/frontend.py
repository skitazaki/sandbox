#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
import urllib2

from nose.tools import ok_, eq_

FRONTEND = 'http://localhost/~shigeru/simple-doc-search'


def test_site():
    url = FRONTEND + '/sites.php'
    r = urllib2.urlopen(url)
    ret = json.load(r)
    pprint(ret)
    ok_('offset' in ret)
    eq_(ret['offset'], 0)
    ok_('data' in ret)
    sites = ret['data']
    eq_(len(sites), 3)
    num, title, url = sites[0]
    eq_(int(num), 1)
    num, title, url = sites[1]
    eq_(int(num), 2)
    num, title, url = sites[2]
    eq_(int(num), 3)

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
