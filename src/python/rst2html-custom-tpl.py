#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog {manuscript}

Parse a reST manuscript and write out it in two way HTML formats.
A file whose suffix is ".html" is for preview, and a file whose suffix
is ".txt" is for blogger's article.
"""

import os
import tempfile

from docutils.core import publish_cmdline

from sandboxlib import parse_args, check_file_path

# see: lib/python2.7/site-packages/docutils/writers/html4css1/template.txt
RST_TEMPLATE_SOURCE = '''
%(body)s
'''


def publish_restructured_text(manuscript):
    fname = tempfile.mktemp()
    with open(fname, 'w') as temp:
        temp.write(RST_TEMPLATE_SOURCE)
    basic_option = ['--strip-comments']
    basename, _ = os.path.splitext(os.path.basename(manuscript))
    source = '%s.txt' % (basename,)
    preview = '%s.html' % (basename,)
    argv = ['--template=%s' % (fname,), manuscript, source]
    publish_cmdline(writer_name='html', argv=basic_option+argv)
    argv = [manuscript, preview]
    publish_cmdline(writer_name='html', argv=basic_option+argv)
    os.unlink(fname)
    print "Write as single HTML page and only body element."
    print "  single page : %s (%dbytes)" % (preview, os.path.getsize(preview))
    print "  only body   : %s (%dbytes)" % (source, os.path.getsize(source))


def main():
    opts, files = parse_args(doc=__doc__, postfook=check_file_path)

    for fname in files:
        publish_restructured_text(fname)


def test():
    manuscript = "../../ChangeLog"
    publish_restructured_text(manuscript)

    assert os.path.exists('ChangeLog.txt')
    assert os.path.exists('ChangeLog.html')

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
