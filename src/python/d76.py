#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """\
python %prog [options] {wikipedia-abstract.xml}

Parse dumped XML data from Wikipedia.
You can download XML file from `here
<http://dumps.wikimedia.org/jawiki/latest/>`_.
"""

import collections
import logging
import optparse
import xml.sax
from xml.sax.handler import ContentHandler


def parse_args():
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-v", "--verbose", dest="verbose",
            default=False, action="store_true", help="verbose mode")
    parser.add_option("-q", "--quiet", dest="verbose",
            default=True, action="store_false", help="quiet mode")

    opts, args = parser.parse_args()

    if len(args) != 1:
        parser.error("Give me a wikipedia abstract xml.")

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)

    return args[0]


class WikipediaAbstractParser(ContentHandler):

    _mode = None
    _counter = 0

    callbacks = []

    targets = ("title", "url", "abstract")

    def startElement(self, name, attrs):
        if name == "doc":
            self._doc = collections.defaultdict(str)
        elif name in self.targets:
            self._mode = name

    def endElement(self, name):
        if name == "doc":
            t = self._doc["title"].replace("Wikipedia: ", "")
            if t:
                self._doc["title"] = t
                for cb in self.callbacks:
                    cb(self._doc)
                self._counter += 1
                logging.debug("Parsed %d items. Current title is \"%s\"" %
                        (self._counter, t))
            self._doc = None
            self._mode = None

    def characters(self, content):
        c = content.strip()
        if self._mode and c:
            self._doc[self._mode] += c

    def add_callback(self, callback):
        self.callbacks.append(callback)
        logging.debug("Add callback, current callbacks are %d." %
                (len(self.callbacks),))


def main():

    def handler(doc):
        title = doc["title"] or ""
        url = doc["url"] or ""
        abstract = doc["abstract"] or ""
        print """<div class="article">
<a href="%s">%s</a><p>%s</p></div>""" % (url, title, abstract)

    target_file = parse_args()
    parser = WikipediaAbstractParser()
    parser.add_callback(handler)
    xml.sax.parse(target_file, parser)

if __name__ == "__main__":
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
