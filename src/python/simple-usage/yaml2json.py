#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options] yaml1 [yaml2 [ ... ]]

Convert data from YAML to JSON.
"""

import logging
import json

import yaml

from sandboxlib import parse_args, check_file_path


def yaml2json(fname):
    try:
        cfg = yaml.load(open(fname))
        print json.dumps(cfg, indent=2)
    except:
        logging.error("Invalid YAML file: %s", fname)


def main():
    opts, files = parse_args(doc=__doc__, postfook=check_file_path)
    for fname in files:
        yaml2json(fname)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
