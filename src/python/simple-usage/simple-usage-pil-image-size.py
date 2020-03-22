#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog image1 [image2 [ ... ]]

Show image size, to require PIL.
"""

import logging
try:
    import Image
except ImportError:
    raise SystemExit("Install PIL (Python Imaging Library) at first.")

from sandboxlib import parse_args, check_file_path


def showimagesize(fname):
    try:
        image = Image.open(fname)
        print "%s: width=%dpx, height=%dpx" % (
                fname, image.size[0], image.size[1])
    except:
        logging.error('"%s" is invalid image file.', fname)

def main():
    opts, files = parse_args(doc=__doc__, postfook=check_file_path)
    for fname in files:
        showimagesize(fname)

if __name__ == '__main__':
    main()

# vim: set expandtab tabstop=4 shiftwidth=4 cindent :
