#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """
Parse a configuration file written in YAML, and extract given section.
The output is Python script so that you can use it as Python module.

Usage::

    $ python yaml2config.py ../../etc/config.yaml production
"""

import optparse
import os.path
from pprint import pprint

import yaml

DEFAULT_CONFIG_VARIABLE = 'CONFIG'


def parse_args():
    parser = optparse.OptionParser(__doc__)
    opts, args = parser.parse_args()
    return opts, args


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


def main():
    _, args = parse_args()

    if len(args) != 2:
        msg = "ERROR: Invalid argument(s).\n" + __doc__
        raise SystemExit(msg)

    fname, section = args
    if not os.path.exists(fname):
        msg = "%s is not found." % (fname,)
        raise SystemExit(msg)
    try:
        config = yaml.load(open(fname))
    except yaml.scanner.ScannerError, e:
        print e
        msg = "%s is invalid YAML format file." % (fname,)
        raise SystemExit(msg)

    if not section in config:
        msg = "%s is not defined in %s." % (section, fname)
        raise SystemExit(msg)

    print "#"
    print "# Configuration for %s environment." % (section,)
    print "#"
    s = config[section]
    dumps(section, s)

if __name__ == '__main__':
    main()

# vim: set expandtab tabstop=4 shiftwidth=4 cindent :