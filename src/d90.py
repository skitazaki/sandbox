#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ == """\
python %prog {manuscript}

Convert reST into HTML text with default template and custom one.

:Usage:
    $ python article.rst
"""

import logging
import optparse
import os.path
import sys

from docutils.core import publish_cmdline

HTML_PREVIEW = "d90.html"
HTML_SOURCE = "d90.txt"
RST_TEMPLATE_SOURCE = "d90.tpl"


def parse_args():
    parser = optparse.OptionParser(__doc__)

    opts, args = parser.parse_args()

    if not args:
        parser.error("no arguments found.")

    return args[0]


def publish_restructured_text(manuscript):
    argv = ["--template=%s" % (RST_TEMPLATE_SOURCE,), manuscript, HTML_SOURCE]
    publish_cmdline(writer_name='html', argv=argv)
    argv = [manuscript, HTML_PREVIEW]
    publish_cmdline(writer_name='html', argv=argv)


def main():
    manuscript = parse_args()

    if not os.path.exists(manuscript):
        logging.fatal("%s is not found." % (manuscript,))
        sys.exit(1)

    publish_restructured_text(manuscript)


def test():
    manuscript = "../ChangeLog"
    publish_restructured_text(manuscript)

    assert os.path.exists(HTML_PREVIEW)
    assert os.path.exists(HTML_SOURCE)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
