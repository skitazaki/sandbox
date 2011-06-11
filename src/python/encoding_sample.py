#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """\
python %prog

Check output encoding, see Appendix 1.2 of Expert Python Programming.
If your output is redirected into file, output encoding is set `None`.

Usage ::

    $ python encoding_sample.py
    $ python encoding_sample.py >encoding_sample.txt
    $ cat encoding_sample.txt
"""

import locale
import sys


def show_io_info(label, desc):
    print label, "descriptor", desc.fileno()
    print label, "encoding", desc.encoding


def main():
    show_io_info("stdin", sys.stdin)
    show_io_info("stdout", sys.stdout)
    show_io_info("stderr", sys.stderr)
    print "preferred locale", locale.getpreferredencoding()
    print "file system", sys.getfilesystemencoding()

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
