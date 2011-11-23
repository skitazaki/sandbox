#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options] solr-schema.xml

Parse schema file of Solr.
"""

import logging
import xml.sax

from string import Template
from xml.sax.handler import ContentHandler

from sandboxlib import parse_args, check_file_path


class SolrSchemaParser(ContentHandler):

    callbacks = []

    targets = ("name", "type", "stored", "indexed")

    def startElement(self, name, attrs):
        if name == "field":
            self._doc = {}
            for n in attrs.getNames():
                self._doc[n] = attrs.get(n)

    def endElement(self, name):
        if name == "field":
            # Check integrity of _doc against self.targets.
            for k in self.targets:
                if not self._doc.has_key(k):
                    logging.warn("%s is missing." % (k,))
            for cb in self.callbacks:
                cb(self._doc)
            self._doc = None

    def add_callback(self, callback):
        self.callbacks.append(callback)
        logging.debug("Add callback, current callbacks are %d." %
                (len(self.callbacks),))

def main():
    # This is a Confuluence table style.
    header = Template("""\
||Attribute Name ||Field Name ||Field Type ||Indexed ||Stored ||Multi Valued |""")
    body = Template("""| Edit on your own | $name | $type | \
$indexed | $stored | $multiValued |""")
    footer = Template("")

    class Processor(object):

        # Output style to organize table layout.
        style = {"header":None, "body":None, "footer":None}

        count = 0

        def leading(self):
            if self.style["header"]:
                print self.style["header"].substitute({})

        def trailing(self):
            if self.style["footer"]:
                print self.style["footer"].substitute({})

        def process(self, doc):
            self.count += 1
            # TODO: Use 1st, 2nd, 3rd, and so forth.
            logging.debug("Processing %dth item." % (self.count,))
            if not doc.has_key("multiValued"):
                doc["multiValued"] = ""
            if self.style["body"]:
                print self.style["body"].safe_substitute(doc)

    opts, files = parse_args(doc=__doc__, postfook=check_file_path)

    processor = Processor()
    processor.style["header"] = header
    processor.style["body"] = body
    parser = SolrSchemaParser()
    parser.add_callback(processor.process)
    processor.leading()
    for fname in files:
        xml.sax.parse(fname, parser)
    processor.trailing()

if __name__ == "__main__":
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :

