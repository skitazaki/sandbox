#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options] {LANDSCAPE.XML}

Convert XML data into CSV file.
Get the public XML data of Sabae City::

    $ curl "http://www3.city.sabae.fukui.jp/ls/landscape.xml" >sabae-landscape.xml
"""

import codecs
import logging
import sys
from xml.etree.ElementTree import ElementTree

from sandboxlib import parse_args, check_file_path

LANDSCAPE_DATA = "http://www3.city.sabae.fukui.jp/ls/landscape.xml"


class Xml2Csv(object):

    def __init__(self, writer=None):
        self.writer = writer or sys.stdout
        self.writer.write("name,longitude,latitude,description\n")

    def process_file(self, fname):
        logging.info("Start processing: %s", fname)
        tree = ElementTree()
        try:
            tree.parse(fname)
            self.process(tree)
        except Exception, e:
            logging.error(e)
        logging.info("End processing: %s", fname)

    def process(self, tree):
        for landscape in tree.iter('landscape'):
            data = {}
            for e in landscape.iter():
                if e.text.strip():
                    data[e.tag] = e.text.strip()
            self.writer.write("%s,%s,%s,%s\n" % (data['title'],
                 data['longitude'], data['latitude'], data['description']))


def main():
    opts, files = parse_args(doc=__doc__, postfook=check_file_path)
    writer = None
    if opts.output:
        writer = codecs.open(opts.output, 'w', opts.enc_out)
    p = Xml2Csv(writer)
    for fname in files:
        p.process_file(fname)
    if writer:
        writer.close()


def test():
    SAMPLE = """
<?xml version="1.0" encoding="UTF-8"?>
<dataroot xmlns:od="urn:schemas-microsoft-com:officedata" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  xsi:noNamespaceSchemaLocation="landscape.xsd" generated="2012-02-03T13:43:42">
<landscape>
<no>1</no>
<city>鯖江市</city>
<title>きらめきロード中河</title>
<location>上河端町、浅水川堤防沿い</location>
<latitude>35.95254</latitude>
<longitude>136.207561</longitude>
<feature>水辺</feature>
<season>春</season>
<description>鯖江市の東部を流れる浅水川の堤防沿いの通り。桜並木と地域の人々が植えた水仙が美しい花を咲かせます。4月上旬～中旬の頃が特に美しい景観となります。</description>
<url>http://www3.city.sabae.fukui.jp/ls#1</url>
<imageurl>http://www3.city.sabae.fukui.jp/ls/image/No1.jpg</imageurl>
<imagelargeurl>http://www3.city.sabae.fukui.jp/ls/imagelarge/No1.jpg</imagelargeurl>
</landscape>
<landscape>
<no>2</no>
<city>鯖江市</city>
<title>三床山</title>
<location>石生谷町ほか</location>
<latitude>35.947476</latitude>
<longitude>136.129267</longitude>
<feature>里山農村</feature>
<season>春</season>
<description>鯖江市の西部にある標高280mの山で御床山とも書きます。古くから要塞の地で、山頂二は延喜式神名帳にも記述のある佐々牟志神社が鎮座し山城跡も残っています。</description>
<url>http://www3.city.sabae.fukui.jp/ls#2</url>
<imageurl>http://www3.city.sabae.fukui.jp/ls/image/No2.jpg</imageurl>
<imagelargeurl>http://www3.city.sabae.fukui.jp/ls/imagelarge/No2.jpg</imagelargeurl>
</landscape>
</dataroot>
    """.strip()
    EXPECTED = u"""name,longitude,latitude,description
きらめきロード中河,136.207561,35.95254,鯖江市の東部を流れる浅水川の堤防沿いの通り。桜並木と地域の人々が植えた水仙が美しい花を咲かせます。4月上旬～中旬の頃が特に美しい景観となります。
三床山,136.129267,35.947476,鯖江市の西部にある標高280mの山で御床山とも書きます。古くから要塞の地で、山頂二は延喜式神名帳にも記述のある佐々牟志神社が鎮座し山城跡も残っています。
    """.strip()
    from StringIO import StringIO
    io = StringIO()
    p = Xml2Csv(io)
    tree = ElementTree()
    tree.parse(StringIO(SAMPLE))
    p.process(tree)
    for e, a in zip(EXPECTED.split('\n'), io.getvalue().split('\n')):
        assert e == a, "expected=%s, actual=%s" % (e, a)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
