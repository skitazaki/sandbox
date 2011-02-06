#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """\
python %prog [options] file

Parses HTML file downloaded from Google Bookmarks.
Since the file is invalid XML, I use `BeautifulSoup` to parse it.
"""

import logging
import optparse
import os.path
import sys

from BeautifulSoup import BeautifulSoup


def parse_args():
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-v", "--verbose", dest="verbose",
            default=False, action="store_true", help="verbose mode")
    parser.add_option("-q", "--quiet", dest="verbose",
            default=True, action="store_false", help="quiet mode")

    opts, args = parser.parse_args()

    if not args:
        parser.error("no parsing file is specified.")

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)

    return args[0]


def process(stream, writer=sys.stdout):
    soup = BeautifulSoup(stream)

    for title in soup.findAll('h3'):
        #print >>writer, title.text
        items = title.nextSibling.nextSibling
        for item in items.findAll('a'):
            if item.text:
                print >>writer, '"%s","%s"' % (item.text, item['href'])


def main():
    fname = parse_args()

    process(open(fname))


def test():
    sample = '''\
<!DOCTYPE NETSCAPE-Bookmark-file-1>
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
    from StringIO import StringIO
    import csv
    io = StringIO()
    process(sample, io)
    io.seek(0)
    for row in csv.reader(io):
        print row
        assert len(row) == 2

if __name__ == "__main__":
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
