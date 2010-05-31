#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Generate PDF file with table layout
# example:
# $ python d37.py d34.csv d37.pdf
# note:
# (http://www.magitech.org/2006/05/05/getting-started-with-reportlab/)

import csv
import getopt
import os
import os.path
import re
import sys

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors

PAGE_WIDTH, PAGE_HEIGHT = A4
PAGE_FONT_SIZE          = 10
PAGE_TITLE_FONT_SIZE    = PAGE_FONT_SIZE * 1.6

# set Japanese Font metrics
# @see also http://www.reportlab.com/docs/userguide.pdf
#           Section 3.6 Asian Font Support
PAGE_FONT_JP       = "HeiseiMin-W3"
PARAGRAPH_STYLE_JP = ParagraphStyle(name="Normal",
                        fontName=PAGE_FONT_JP,
                        spaceAfter=inch)
pdfmetrics.registerFont(UnicodeCIDFont(PAGE_FONT_JP))

def parse_args():
  usage = """usage: python %s <input-file> <output-file>
input file must be the CSV format for iteration.
  """
  if len(sys.argv) != 3:
    print(usage % (sys.argv[0]))
    sys.exit(1)
  fname = sys.argv[1]
  output = sys.argv[2]
  if not os.path.exists(fname):
    print("[ERROR] \"%s\" is not found." % (fname))
    sys.exit(1)
  return csv.reader(open(fname, "rb")), output

# see also ReportLab user guide Chapter 7 Tables and TableStyles
def writepdftable(data, output):
  style = [('FONT', (0, 0), (-1, -1), PAGE_FONT_JP),
           ('GRID', (0, 0), (-1, -1), 1, colors.black)]
  # a container of flowable objects.
  elements = []
  elements.append(Paragraph("表のテスト", PARAGRAPH_STYLE_JP))
  elements.append(Table(data, style=style))
  SimpleDocTemplate(output).build(elements)

def main():
  input, output = parse_args()
  data = [row for row in input]
  writepdftable(data, output)

if __name__ == '__main__':
  main()

# vim: set et ts=2 sw=2 cindent fileencoding=utf-8 :

