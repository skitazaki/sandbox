#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog image1 [image2 [ ... ]]

Show image data information as JSON format.
require Python 2.6 or higher and PIL module.
"""

import os
import logging
try:
    import json
except ImportError:
    raise SystemExit("Use Python 2.6 or higher.")
try:
    import Image
except ImportError:
    raise SystemExit("Install PIL (Python Imaging Library) at first.")

from sandboxlib import parse_args, check_file_path


def getimageinfo(fname):
    try:
        image = Image.open(fname)
        size = image.size
    except:
        logging.error('"%s" is invalid image file.', fname)
        size = None
    return {'name': os.path.basename(fname),
            'path': os.path.abspath(fname),
            'size': size}


def main():
    opts, files = parse_args(doc=__doc__, postfook=check_file_path)
    images = [getimageinfo(f) for f in files]
    print json.dumps(images)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
