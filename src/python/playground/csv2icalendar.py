#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""\
python %prog [options] csvfile [, csvfile [,csvfile ...]]

Sample script to write out iCalendar file using `icalendar` module.
`#fctokyo <http://www.fctokyo.co.jp/home/index.phtml?cont=result/top_team>`_
"""

import csv
from datetime import datetime, timedelta
import logging
import optparse
import os.path
import sys
import uuid

from icalendar import Calendar, Event, Timezone


def parse_args():
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-v", "--verbose", dest="verbose",
            default=False, action="store_true", help="verbose mode")
    parser.add_option("-q", "--quiet", dest="verbose",
            default=True, action="store_false", help="quiet mode")

    opts, args = parser.parse_args()

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)

    return opts, args


class CalendarWrap(object):

    def __init__(self):
        cal = Calendar()
        cal['method'] = 'PUBLISH'
        cal['prodid'] = '-//S.Kitazaki//Python Sample//'
        cal['version'] = '2.0'
        cal['X-WR-CALNAME'] = '#fctokyo2011'
        cal['X-WR-TIMEZONE'] = 'Asia/Tokyo'
        tz = Timezone()
        tz['TZID'] = 'Asia/Tokyo'
        tz['X-LIC-LOCATION'] = 'Asia/Tokyo'
        tz['TZOFFSETFROM'] = '+0900'
        tz['TZOFFSETTO'] = '+0900'
        tz['TZNAME'] = 'JST'
        tz['DTSTART'] = '19700101T000000'
        cal.add_component(tz)
        self.cal = cal

    def _add(self, data):
        event = Event()
        event['uid'] = uuid.uuid4().hex
        event['summary'] = data['ホーム'] + ' vs. ' + data['アウェイ']
        event['location'] = data['会場']
        if data['TV中継']:
            event['description'] = data['TV中継']
        y = 2011
        m, d = [int(i) for i in data['開催日'].split('/')]
        if data['キックオフ']:
            H, M = [int(i) for i in data['キックオフ'].split(':')]
            d = datetime(y, m, d, H, M)
            e = d + timedelta(hours=2)
            event.set('dtend', e)
        else:
            d = datetime(y, m, d)
        event.set('dtstart', d)
        logging.debug("New event is " + event.as_string())
        self.cal.add_component(event)

    def add(self, stream):
        header = stream.next()
        logging.debug("Processing header, %s" % ('\t'.join(header),))
        for line in stream:
            if len(header) == len(line):
                data = dict(zip(header, line))
                self._add(data)

    def write(self, writer):
        print >>writer, self.cal.as_string()


def main():
    opts, args = parse_args()

    c = CalendarWrap()

    for fname in args:
        if not os.path.exists(fname):
            logging.error("'%s' is not found." % (fname,))
            continue
        logging.info("Start processing '%s'." % (fname,))
        fp = open(fname, 'rb')
        c.add(csv.reader(fp))
        fp.close()

    import sys
    c.write(sys.stdout)


def test():
    DATA = u'''開催日,キックオフ,ホーム,アウェイ,会場,結果,TV中継
3/5,14:00,FC東京,サガン鳥栖,味の素スタジアム,,スカパー/e2/スカパー光/ひかりTV TOKYO MX
'''
    from StringIO import StringIO
    istream = StringIO(DATA)
    ostream = StringIO()

    c = CalendarWrap()
    c.add(csv.reader(istream))
    c.write(ostream)
    ostream.seek(0)
    print ostream.read()
    '''
    BEGIN:VCALENDAR
    METHOD:PUBLISH
    PRODID:-//S.Kitazaki//Python Sample//
    VERSION:2.0
    X-WR-CALNAME:#fctokyo2011
    X-WR-TIMEZONE:Asia/Tokyo
    BEGIN:VTIMEZONE
    DTSTART:19700101T000000
    TZID:Asia/Tokyo
    TZNAME:JST
    TZOFFSETFROM:+0900
    TZOFFSETTO:+0900
    X-LIC-LOCATION:Asia/Tokyo
    END:VTIMEZONE
    BEGIN:VEVENT
    DESCRIPTION:スカパー/e2/スカパー光/ひかりTV TOKYO MX
    DTEND;VALUE=DATE:20110305T160000
    DTSTART;VALUE=DATE:20110305T140000
    LOCATION:味の素スタジアム
    SUMMARY:FC東京 vs. サガン鳥栖
    UID:ab72640619f54c2ebd5e83548a1efa5a
    END:VEVENT
    END:VCALENDAR
    '''
    assert False

if __name__ == "__main__":
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
