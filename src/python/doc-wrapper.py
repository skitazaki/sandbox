#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Wrap HTML document generated from rst2html.

Usage:
    ./doc-wrapper.py {input_file} {output_file}
"""

from __future__ import with_statement
import re
import os
import sys
from string import Template
from cStringIO import StringIO

TPL = """{% extends "base.html" %}

{% block title %}Books - $title{% endblock %}

{% block contents %}
$contents
{% endblock %}"""

START_MARKER = '<body>'
END_MARKER = '</body>'
TITLE_PATTERN = re.compile('<h1 class="title">(.+)</h1>')


class Processor(object):

    def __init__(self, template):
        self.template = Template(template)
        self.writer = StringIO()
        self.in_process = False

    def process(self, line):
        if line == START_MARKER:
            self.in_process = True
            return
        elif line == END_MARKER:
            self.in_process = False

        if not self.in_process:
            return

        m = TITLE_PATTERN.match(line)
        if m:
            self.title = m.group(1)
            return
        self.writer.write(line + '\n')

    def to_string(self):
        return self.template.substitute(title=self.title,
                contents=self.writer.getvalue())


def main():
    argv = sys.argv[1:]
    if len(argv) != 2:
        raise SystemExit('See usage.\n' + __doc__)
    fname, output = argv
    if not os.path.exists(fname):
        raise SystemExit('"%s" is not found.' % (fname,))
    if os.path.exists(output):
        raise SystemExit('"%s" already exists.' % (output,))
    processor = Processor(TPL)
    with open(fname) as fp:
        for line in fp:
            processor.process(line.rstrip())
    with open(output, 'w') as writer:
        writer.write(processor.to_string())

if __name__ == '__main__':
    main()
