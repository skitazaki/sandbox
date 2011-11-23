#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options] file

Parses HTML file downloaded from Google Bookmarks.
Since the file is invalid XML, I use `BeautifulSoup` to parse it.
"""

import csv
import logging
import sys

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    raise SystemExit("`BeautifulSoup` module is not found on your system.")

from sandboxlib import parse_args, check_file_path


class HTMLProcessor(object):

    def __init__(self, writer=None):
        w = writer or sys.stdout
        self.writer = csv.writer(w)

    def process_file(self, fname):
        logging.info("Start processing: %s", fname)
        self.process(open(fname))
        logging.info("End processing: %s", fname)

    def process(self, stream):
        soup = BeautifulSoup(stream)
        for title in soup.findAll('h3'):
            #print title.text
            items = title.nextSibling.nextSibling
            for item in items.findAll('a'):
                if item.text:
                    row = (item.text.encode('utf-8'), item['href'])
                    self.writer.writerow(row)


def main():
    opts, files = parse_args(doc=__doc__, postfook=check_file_path)
    p = HTMLProcessor(opts.output)
    for fname in files:
        p.process_file(fname)


def test():
    sample = '''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
<DT><H3 ADD_DATE="1290515442321399">ActiveDirectory</H3>
<DL><p>
<DT><A HREF="http://gihyo.jp/admin/serial/01/ad-linux/0002?page=3" ADD_DATE="1290515442321399">Active DirectoryとLinuxの認証を統合しよう：第2回　SUAのNIS機能による認証統合｜gihyo.jp … 技術評論社</A>
</DL><p>
<DT><H3 ADD_DATE="1240192790148038">AtomPub</H3>
<DL><p>
<DT><A HREF="http://www.tbray.org/ongoing/When/200x/2007/03/22/Atom" ADD_DATE="1240192790148038">ongoing · Rewriting my Gravestone</A>
</DL><p>
<DT><H3 ADD_DATE="1218497870324031">C</H3>
<DL><p>
<DT><A HREF="http://www.cc.ariake-nct.ac.jp/~bashi/tips/gdb/sec1.html" ADD_DATE="1239178230567696">GDB を使ってプログラムを動かしてみる</A>
<DT><A HREF="http://labs.unoh.net/2008/11/diff_with_c.html" ADD_DATE="1227194692754678">ウノウラボ Unoh Labs: diff with C++</A>
<DD>diff
<DT><A HREF="http://www.nurs.or.jp/~sug/soft/super/" ADD_DATE="1231218908696900">Super Technique 講座〜目次</A>
<DT><A HREF="http://www.varnish-cache.org/" ADD_DATE="1276825649934775">Varnish</A>
<DT><A HREF="http://www.aerith.net/technical-j.html" ADD_DATE="1218497879216000">ソフトウェア工学</A>
<DT><A HREF="http://www.wangafu.net/~nickm/libevent-book/" ADD_DATE="1264841659525247">Fast portable non-blocking network programming with Libevent</A>
<DT><A HREF="http://www.nurs.or.jp/~sug/soft/super/bash.htm" ADD_DATE="1231218879947769">Super Technique 講座〜bash 超プログラム術</A>
<DT><A HREF="http://nanika.osonae.com/" ADD_DATE="1218497870324031">C / C++ / C#</A>
</DL><p>'''
    from cStringIO import StringIO
    io = StringIO()
    p = HTMLProcessor(io)
    p.process(sample)
    io.seek(0)
    for row in csv.reader(io):
        print row
        assert len(row) == 2

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
