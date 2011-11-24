#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options] file1 [file2 [ ... ]]

Convert CSV file into KML format.
See KML Tutorial
<http://code.google.com/intl/ja/apis/kml/documentation/kml_tut.html>

Input file must contain following header line:

    name,latitude,longitude,description
"""

import codecs
import csv
import logging
import sys

try:
    import jinja2
except ImportError:
    raise SystemExit("`jinja2` module is not found on your system.")

from sandboxlib import parse_args, check_file_path

TEMPLATE = u"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
{% for point in points %}
  <Placemark>
    <name>{{ point.name }}</name>
    {% if point.description %}
    <description>{{ point.description }}</description>
    {% endif %}
    <Point>
      <coordinates>{{ point.latitude }},{{ point.longitude }}</coordinates>
    </Point>
  </Placemark>
{% endfor %}
</kml>"""


class Renderer(object):

    writer = None

    def __init__(self, output=None, encoding=None):
        if output:
            if encoding:
                self.writer = codecs.open(output, 'w', encoding)
            else:
                self.writer = open(output, 'w', encoding)

    def render(self, points):
        template = jinja2.Template(TEMPLATE)
        s = template.render(points=points)
        if self.writer:
            self.writer.write(s)
            self.writer.close()
        else:
            print s

class Processor(object):

    def __init__(self, rederer):
        self.rederer = rederer

    def process_file(self, fname, encoding):
        logging.info("Start processing: %s", fname)
        try:
            self.process(codecs.open(fname, 'rb', encoding=encoding))
            logging.info("End processing: %s", fname)
        except Exception, e:
            logging.error(e)

    def process(self, reader):
        header = reader.next().strip().split(',')
        points = []
        for line in reader:
            r = line.strip()
            if not r:
                continue
            row = r.split(',')
            data = dict(zip(header, row))
            points.append(data)
        self.rederer.render(points)


def main():
    opts, files = parse_args(doc=__doc__, postfook=check_file_path)
    p = Processor(Renderer(opts.output, opts.enc_out))
    for fname in files:
        p.process_file(fname, opts.enc_in)


def test():
    SAMPLE = u"""name,latitude,longitude,description
国立霞ヶ丘競技場,139.714941,35.678160,naash.go.jp
"""
    from StringIO import StringIO
    sample = StringIO(SAMPLE)
    sample.seek(0)
    p = Processor(Renderer())
    p.process(sample)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :

