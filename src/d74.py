#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Read these links:
# * http://www.adobe.com/jp/devnet/air/articles/use_air_extension.html
# * http://help.adobe.com/ja_JP/AIR/1.1/devappshtml/WS5b3ccc516d4fbf351e63e3d118666ade46-7ecc.html
# * http://www.adobe.com/support/documentation/jp/air/2/releasenotes_developers.html

__doc__ = """\
python %prog [options] project_name

Start up script for Adobe AIR SDK.
Create directory and prepare fundamental files.
"""

import logging
import optparse
import os
import os.path
import shutil
import sys

# TODO switch base directory along with Operating Systems automatically.
# for Windows
#BASEDIR = "C:/Program Files (x86)/Adobe/AdobeAIRSDK"
# for Linux
#BASEDIR = "/usr/local/AdobeAIRSDK"
# for MacOSX
BASEDIR = "/Applications/Adobe/AdobeAIRSDK"


def parse_args():
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-d", "--basedir", dest="basedir", default=BASEDIR,
            help="Base direcotry of AIR SDK")

    opts, args = parser.parse_args()

    if len(args) != 1:
        parser.error("I can accept only one argument.")

    return opts.basedir, args[0]


def project_starter(sdkdir, project):
    os.mkdir(project)

    # TODO edit <id>, <filename>, <name>, and <initialWindow>.
    shutil.copy(os.path.join(sdkdir, "templates", "air", "descriptor-template.xml"),
            os.path.join(project, "application.xml"))

    shutil.copy(os.path.join(sdkdir, "frameworks", "libs", "air", "AIRAliases.js"),
            os.path.join(project, "AIRAliases.js"))

    toppage = open(os.path.join(project, "%s.html" % (project,)), "wb")
    toppage.write("""
<html>
<head>
<title>%s</title>
<script type="text/javascript" src="AIRAliases.js"></script>
<script type="text/javascript">
function appLoad(){
    air.trace("Hello World");
    var xhr = new XMLHttpRequest();
    // do some cool stuff :D
}
</script>
</head>
<body onLoad="appLoad()">
<h1>Hello World</h1>
<div id="content"></div>
</body></html>
""" % (project,))
    toppage.close()
    # TODO put build script as `Makefile` or `ant`.
    adt = os.path.join(sdkdir, "bin", "adt")
    adl = os.path.join(sdkdir, "bin", "adl")
    print "%s application.xml" % (adl,)
    print "%s -certificate -cn SelfSigned 1024-RSA sampleCert.pfx samplePassword" % (adt,)
    print "%s -package -certificate sampleCert.pfx -password samplePassword \
            %s.air application.xml %s.html AIRAliases.js" % (adt, project, project)


def main():
    sdkdir, project = parse_args()

    if not os.path.exists(sdkdir):
        logging.fatal("AIR SDK is not found in \"%s\"" % (sdkdir,))
        sys.exit(1)

    if os.path.exists(project):
        logging.fatal('''project named "%s" already exists.''' % (project,))
        sys.exit(1)

    try:
        project_starter(sdkdir, project)
    except Exception, e:
        logging.fatal(e)
        sys.exit(255)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
