# -*- coding: utf-8 -*-

"""Parse schema file of Solr.
"""

import logging
import xml.sax

from string import Template
from xml.sax.handler import ContentHandler

from sandboxlib import parse_args, setup_fileio, check_file_path


# This is a Confuluence table style.
STYLE = {
    "header": """\
||Attribute Name ||Field Name ||Field Type ||Indexed ||Stored ||Multi Valued |""",
    "body": """| Edit on your own | $name | $type | \
$indexed | $stored | $multiValued |""",
    "footer": None,
}


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
                if k not in self._doc:
                    logging.warn(f"{k} is missing.")
            for cb in self.callbacks:
                cb(self._doc)
            self._doc = None

    def add_callback(self, callback):
        self.callbacks.append(callback)
        logging.debug(f"Added a callback, and current list has {len(self.callbacks)}.")


class Processor(object):

    # Output style to organize table layout.
    style = {"header": None, "body": None, "footer": None}

    count = 0

    def __init__(self, header, body, footer):
        if header:
            self.style["header"] = Template(header)
        if body:
            self.style["body"] = Template(body)
        if footer:
            self.style["footer"] = Template(footer)

    def leading(self):
        if self.style["header"]:
            print(self.style["header"].substitute({}))

    def trailing(self):
        if self.style["footer"]:
            print(self.style["footer"].substitute({}))

    def process(self, doc):
        self.count += 1
        # TODO: Use 1st, 2nd, 3rd, and so forth.
        logging.debug(f"Processing {self.count}th item.")
        if "multiValued" not in doc:
            doc["multiValued"] = ""
        if self.style["body"]:
            print(self.style["body"].safe_substitute(doc))


def main():
    args = parse_args(doc=__doc__, prehook=setup_fileio, posthook=check_file_path)

    processor = Processor(**STYLE)
    parser = SolrSchemaParser()
    parser.add_callback(processor.process)
    processor.leading()
    files = args.files
    for fname in files:
        xml.sax.parse(fname, parser)
    processor.trailing()


if __name__ == "__main__":
    main()
