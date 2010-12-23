#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Show image data information as JSON format.
# (copy from d14.py and require Python 2.6)
# example:
# $ python d43.py a.jpg b.jpg c.jpg

import os.path
import sys
try:
    import json
except ImportError:
    print "Use Python 2.6 or higher."
    sys.exit(255)
try:
    import Image
except ImportError:
    print "Install PIL (Python Imaging Library) at first."
    sys.exit(255)


def parse_args():
    usage = """usage: python %s image_file [image_file..]"""
    if len(sys.argv) < 2:
        print usage % (sys.argv[0])
        sys.exit(1)
    return sys.argv[1:]


def getimageinfo(fname):
    try:
        image = Image.open(fname)
    except:
        sys.stderr.write("invalid image: %s\n" % (fname))
    return {'name': os.path.basename(fname),
            'path': os.path.abspath(fname),
            'size': image.size}


def main():
    files = parse_args()
    images = []
    for f in files:
        if os.path.exists(f):
            images.append(getimageinfo(f))
        else:
            sys.stderr.write('"%s" is not found.\n' % (f))
    print json.dumps(images)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
