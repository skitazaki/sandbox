#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options] {yaml_file} {section_name}

Parse a configuration file written in YAML, and extract given section.
The output is Python script so that you can use it as Python module.

Usage::

    $ python yaml2config.py ../../etc/config.yaml production
"""

import logging
import os
from pprint import pprint

import yaml

from sandboxlib import parse_args, ArgumentError

DEFAULT_CONFIG_VARIABLE = 'CONFIG'


def dumps(name, s):
    t = type(s)
    if t == int:
        print '%s = %d' % (DEFAULT_CONFIG_VARIABLE, s)
    elif t == str:
        print '%s = "%s"' % (DEFAULT_CONFIG_VARIABLE, s)
    elif t == dict:
        for k in s:
            print k.upper(), '= ',
            pprint(s[k])
    else:
        print DEFAULT_CONFIG_VARIABLE, '= ',
        pprint(s)


def postfook(opts, args):
    if len(args) != 2:
        raise ArgumentError("Missing arguments.")
    fname, section = args
    if not os.path.exists(fname):
        msg = "%s is not found." % (fname,)
        raise ArgumentError(msg)


def main():
    opts, args = parse_args(doc=__doc__, postfook=postfook)

    fname, section = args
    try:
        config = yaml.load(open(fname))
    except yaml.scanner.ScannerError, e:
        logging.error("%s is invalid YAML format file.", fname)
        return

    if not section in config:
        logging.error("%s is not defined in %s.", section, fname)
        return

    print "#"
    print "# Configuration for %s environment." % (section,)
    print "#"
    s = config[section]
    dumps(section, s)

if __name__ == '__main__':
    main()

# vim: set expandtab tabstop=4 shiftwidth=4 cindent :
