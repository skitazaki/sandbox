#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """\
python %prog {project_name}

Download `HTML 5 boilerplace package
<http://html5boilerplace.com>`_ and unpack it.
"""

import optparse
import os
import os.path
import sys
import time
import urllib2
import zipfile
import StringIO


def parse_args():
    parser = optparse.OptionParser(__doc__)
    opts, args = parser.parse_args()

    if len(args) != 1:
        parser.error("I can accept only one argument.")

    return args[0]

PACKAGE = "http://github.com/paulirish/html5-boilerplate/zipball/v0.9.1stripped"


def project_starter(project):
    os.mkdir(project)
    current_time = time.time()
    try:
        response = urllib2.urlopen(PACKAGE)
    except urllib2.URLError, e:
        raise
    if response.getcode() == 200:
        # since `response` does not have `seek` property, convert it into
        # file-style-object with `StirngIO`.
        file = StringIO.StringIO(response.read())
        zipfile.ZipFile(file).extractall(project)
        for d in os.listdir(project):
            path = os.path.join(project, d)
            if os.path.isdir(path) and current_time < os.path.getctime(path):
                os.rename(path, os.path.join(project, "src"))
    else:
        print >>sys.stderr, """fail to download archive package from %s.
check your internet connection and try again.
the response header is:
%s
""" % (PACKAGE, response.info())
        raise IOError


def main():
    project = parse_args()
    if os.path.exists(project):
        print >>sys.stderr, \
            '''project named "%s" already exists.''' % (project,)
        sys.exit(1)

    try:
        project_starter(project)
    except Exception, e:
        print >>sys.stderr, e
        sys.exit(1)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
