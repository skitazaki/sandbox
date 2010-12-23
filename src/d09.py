#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Generate PDF file using ReportLab.
# Usage:
# $ python d09.py d09.txt d09.pdf

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


def usage(program):
    print '''Usage:
    python %s input_file_name output_file_name
    ''' % (program)
    import sys
    sys.exit(1)


def copy2pdf(input, output):
    doc = SimpleDocTemplate(output)
    story = []
    t = []
    for line in open(input):
        l = line.strip()
        if l:
            t.append(l)
        elif len(t) > 0:
            p = Paragraph(''.join(t), PARAGRAPH_STYLE_JP)
            story.append(p)
            t = []  # clear for new paragraph
    doc.build(story)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        usage(sys.argv[0])
    copy2pdf(sys.argv[1], sys.argv[2])

# vim: set expandtab tabstop=4 shiftwidth=4 cindent :
