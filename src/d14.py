#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Show image size, to require PIL.
# example:
# $ python d14.py a.jpg

import sys
import Image


def usage(program):
    print '''usage: python %s image_file [image_file..]
    ''' % (program)
    sys.exit(1)


def showimagesize(fname):
    try:
        image = Image.open(fname)
        print "%s: width=%dpx, height=%dpx" % (
                fname, image.size[0], image.size[1])
    except:
        print "could not find: %s" % fname

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage(sys.argv[0])
    for fname in sys.argv[1:]:
        showimagesize(fname)

# vim: set expandtab tabstop=4 shiftwidth=4 cindent :
