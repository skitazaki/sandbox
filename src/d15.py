#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creates thumbnail image(s), to require PIL.
# example:
# $ python d15.py a.jpg

import os.path
import sys
import Image

MINSIZE = (120, 120)
FILENAMEEXT = "thumbnail"

def usage(program):
    print '''usage: python %s image_file [image_file..]
    ''' % (program)
    sys.exit(1)

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

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage(sys.argv[0])
    for fname in sys.argv[1:]:
        createthumbnail(fname)

# vim: set et ts=4 sw=4 cindent :

