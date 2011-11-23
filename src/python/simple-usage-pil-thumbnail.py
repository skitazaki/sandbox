#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog image1 [image2 [ ... ]]

Creates thumbnail image(s), to require PIL.
"""

import logging
import os
try:
    import Image
except ImportError:
    raise SystemExit("Install PIL (Python Imaging Library) at first.")

from sandboxlib import parse_args, check_file_path

MINSIZE = (120, 120)
FILENAMEEXT = "thumbnail"


def createthumbnail(fname):
    def writeout(thumbnail, newname):
        try:
            out = open(newname, "w")
            thumbnail.save(out)
            out.close()
            print "%s %d %d" % (newname, image.size[0], image.size[1])
        except:
            print "could not create a new file: %s" % newname
    try:
        image = Image.open(fname)
        (name, ext) = os.path.splitext(os.path.basename(fname))
        if not ext:
            raise "could not find file extension: %s" % fname
        image.thumbnail(MINSIZE)
        writeout(image, "%s-%s%s" % (name, FILENAMEEXT, ext.lower()))
    except IOError:
        print "could not find: %s" % fname


def main():
    opts, files = parse_args(doc=__doc__, postfook=check_file_path)
    for fname in files:
        createthumbnail(fname)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
