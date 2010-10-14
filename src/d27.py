#!/usr/bin/env python
# -*- coding: utf-8 -*-
# convert data from YAML to JSON

import json
import sys

import yaml
import yaml.scanner

def usage(program):
  print '''usage: python %s YAML[ YAML..]
  ''' % (program)

def yaml2json(fname):
  try:
    print(json.loads(str(yaml.load(open(fname))).replace("'", '"')))
  except yaml.scanner.ScannerError:
    sys.stderr.write("Invalid YAML file: %s\n" % fname)

if __name__ == '__main__':
  if len(sys.argv) == 1:
    usage(sys.argv[0])
    sys.exit(1)
  import os.path
  for fname in sys.argv[1:]:
    if os.path.exists(fname):
      yaml2json(fname)
    else:
      sys.stderr.write("No such file: %s\n" % fname)

# vim: set et ts=2 sw=2 cindent fileencoding=utf-8 :

