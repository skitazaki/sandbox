#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Generate PDF file using ReportLab.
# example:
# $ python d34.py -o output -t d34.txt -f d34.csv

import csv
import getopt
import os
import os.path
import re
import sys

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

PAGE_WIDTH, PAGE_HEIGHT = A4
PAGE_FONT_SIZE = 10
PAGE_TITLE_FONT_SIZE = PAGE_FONT_SIZE * 1.6

# Set Japanese Font metrics.
# @see also http://www.reportlab.com/docs/userguide.pdf
#           Section 3.6 Asian Font Support
PAGE_FONT_JP = "HeiseiMin-W3"
PARAGRAPH_STYLE_JP = ParagraphStyle(name="Normal",
                        fontName=PAGE_FONT_JP,
                        spaceAfter=inch)
pdfmetrics.registerFont(UnicodeCIDFont(PAGE_FONT_JP))


def parse_args():
    usage = """usage: python %s [-o output-dir] -t <template> -f <data-file>
Options:
  -t template file name (mandatory option)
  -f data file name (mandatory option)
  -o directory where generated pdf files are stored in
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:t:o:")
    except getopt.GetoptError:
        print(usage % (sys.argv[0]))
        sys.exit(1)
    fname = None
    tpl = None
    output = os.getcwd()
    for o, v in opts:
        if o == "-f":
            fname = v
        elif o == "-t":
            tpl = v
        elif o == "-o":
            if not os.path.exists(v):
                os.mkdir(v)
            output = v
    if not fname:
        print("[ERROR] \"-f\" option is mandatory.")
        sys.exit(1)
    if not os.path.exists(fname):
        print("[ERROR] \"%s\" not found." % (fname))
        sys.exit(1)
    if not tpl:
        print("[ERROR] \"-t\" option is mandatory.")
        sys.exit(1)
    if not os.path.exists(tpl):
        print("[ERROR] \"%s\" not found." % (tpl))
        sys.exit(1)
    return open(tpl, "rb").read(), csv.reader(open(fname, "rb")), output


def writepdf(text, output):
    doc = SimpleDocTemplate(output)
    story = []
    p = Paragraph(text, PARAGRAPH_STYLE_JP)
    story.append(p)
    doc.build(story)


def main():
    template, data, output = parse_args()
    # ReportLab accepts "<br />" tag as new line instead of "\n"
    template = "<br />".join(template.split("\n"))
    name = re.compile("\$1")
    url = re.compile("\$2")
    for i, r in enumerate(data):
        if r[1].find("www") == 0:
            r[1] = "http://%s" % (r[1])
        text = url.sub(r[1], name.sub(r[0], template))
        writepdf(text, os.path.join(output, "%d.pdf" % (i + 1)))

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
