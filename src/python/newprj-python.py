#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# See also:
# <http://blog.teemu.im/2009/02/08/using-zcbuildout-in-a-twisted-project/>
# <http://code.google.com/p/typhoonae/source/browse/buildout.cfg>

"""python %prog [options] project_name

Creates a Python project using `virtualenv` and `buildout`.
Sample project contains `mongodb`.
"""

import logging
import os
import subprocess
import urllib2
from string import Template

from sandboxlib import parse_args, ArgumentError

BUILDOUT_BOOTSTRAP = \
  "http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py"

BUILDOUT_CFG = """\
[buildout]
parts =
    depends
    mongodb
develop = ./src

[versions]
pymongo = 2.0

[depends]
recipe = minitage.recipe:egg
eggs =
    pyOpenSSL
    pycrypto

[mongodb]
recipe = rod.recipe.mongodb
darwin-32bit-url = http://downloads.mongodb.org/osx/mongodb-osx-i386-1.8.2.tgz
darwin-64bit-url = http://downloads.mongodb.org/osx/mongodb-osx-x86_64-1.8.2.tgz
linux2-32bit-url = http://downloads.mongodb.org/linux/mongodb-linux-i686-1.8.2.tgz
linux2-64bit-url = http://downloads.mongodb.org/linux/mongodb-linux-x86_64-1.8.2.tgz
"""

SETUP_PY = Template("""\
from setuptools import setup, find_packages

setup(
    name='${project}',
    version='0.1.0',
    description='SAMPLE APPLICATION',
    author='Shigeru Kitazaki',
    packages=find_packages('${project}'),
    zip_safe=False
)
""")


def postfook(opts, args):
    if len(args) != 1:
        raise ArgumentError("No project name was given.")
    project = args[0]

    if os.path.exists(project):
        msg = "project named \"%s\" already exists." % (project,)
        raise ArgumentError(msg)

    if "." in project or "/" in project:
        raise ArgumentError("Invalid project name.")


def project_starter(project):
    argv = ['virtualenv', '--distribute', project]
    subprocess.call(argv)

    os.chdir(project)

    with open('buildout.cfg', 'wb') as recipe:
        recipe.write(BUILDOUT_CFG)

    try:
        r = urllib2.urlopen(BUILDOUT_BOOTSTRAP)
        logging.debug(r.info())
        with open('bootstrap.py', 'wb') as bootstrap:
            bootstrap.write(r.read())
    except urllib2.URLError, e:
        logging.error("Could not get %s", BUILDOUT_BOOTSTRAP)
        raise SystemExit("Network problem.")

    argv = [os.path.join('bin', 'python'), 'bootstrap.py']
    subprocess.call(argv)

    with open('README', 'wb') as readme:
        readme.write(project)

    os.mkdir('src')
    os.mkdir(os.path.join('src', project))
    with open(os.path.join('src', project, '__init__.py'), 'wb') as strap:
        strap.write('# -*- coding: utf-8 -*-')
    with open(os.path.join('src', 'setup.py'), 'wb') as setup:
        setup.write(SETUP_PY.substitute(dict(project=project)))

    argv = [os.path.join('bin', 'buildout')]
    subprocess.call(argv)


def main():
    opts, projects = parse_args(doc=__doc__, postfook=postfook)
    project_starter(projects[0])


def test():
    project_starter("test_project")

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf8 :
