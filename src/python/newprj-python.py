#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# See also:
# <http://blog.teemu.im/2009/02/08/using-zcbuildout-in-a-twisted-project/>
# <http://code.google.com/p/typhoonae/source/browse/buildout.cfg>

__doc__ = """\
python %prog [options] project_name

Creates Python project using `virtualenv` and `buildout`.
This project contains `twisted` and `mongodb`.
"""

import logging
import optparse
import os
import os.path
import sys
import subprocess
import urllib2

from string import Template

BUILDOUT_BOOTSTRAP = \
  "http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py"

BUILDOUT_CFG = """\
[buildout]
parts =
    depends
    twisted
    twisteds
    mongodb
develop = ./src

[versions]
Twisted = 10.2.0
pyOpenSSL = 0.11
pycrypto = 2.3
pymongo = 1.9

[depends]
recipe = minitage.recipe:egg
eggs =
    pyOpenSSL
    pycrypto

[twisted]
recipe = minitage.recipe:egg
eggs = Twisted

[mongodb]
recipe = rod.recipe.mongodb
darwin-32bit-url = http://downloads.mongodb.org/osx/mongodb-osx-i386-1.6.5.tgz
darwin-64bit-url = http://downloads.mongodb.org/osx/mongodb-osx-x86_64-1.6.5.tgz
linux2-32bit-url = http://downloads.mongodb.org/linux/mongodb-linux-i686-1.6.5.tgz
linux2-64bit-url = http://downloads.mongodb.org/linux/mongodb-linux-x86_64-1.6.5.tgz

[twisteds]
recipe = minitage.recipe:scripts
interpreter = twistedpy
extra-paths = ${buildout:directory}/src
eggs =
    ${twisted:eggs}
    ${depends:eggs}
"""

SETUP_PY = Template("""\
from setuptools import setup, find_packages

setup(
    name='${project}',
    version='0.1',
    description='SAMPLE APPLICATION',
    author='Shigeru Kitazaki',
    packages=find_packages('${project}'),
    zip_safe=False
)
""")


def parse_args():
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-v", "--verbose", dest="verbose",
            default=False, action="store_true", help="verbose mode")

    opts, args = parser.parse_args()

    if len(args) != 1:
        parser.error("I can accept only one argument.")

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)

    return args[0]


def project_starter(project):
    argv = ["virtualenv", project]
    subprocess.call(argv)

    os.chdir(project)

    recipe = open("buildout.cfg", "wb")
    recipe.write(BUILDOUT_CFG)
    recipe.close()

    try:
        r = urllib2.urlopen(BUILDOUT_BOOTSTRAP)
        logging.debug(r.info())
        bootstrap = open("bootstrap.py", "wb")
        bootstrap.write(r.read())
        bootstrap.close()
    except urllib2.URLError, e:
        raise

    argv = [os.path.join("bin", "python"), "bootstrap.py"]
    subprocess.call(argv)

    readme = open("README", "wb")
    readme.close()

    os.mkdir("src")
    os.mkdir(os.path.join("src", project))
    strap = open(os.path.join("src", project, "__init__.py"), "wb")
    strap.close()
    setup = open(os.path.join("src", "setup.py"), "wb")
    setup.write(SETUP_PY.substitute(dict(project=project)))
    setup.close()

    argv = [os.path.join("bin", "buildout")]
    subprocess.call(argv)


def main():
    project = parse_args()

    if os.path.exists(project):
        logging.fatal('''project named "%s" already exists.''' % (project,))
        sys.exit(1)

    if "." in project or "/" in project:
        logging.fatal("Invalid project name.")
        sys.exit(2)

    try:
        project_starter(project)
    except Exception, e:
        logging.fatal(e)
        sys.exit(255)


def test():
    project_starter("test_project")

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf8 :
