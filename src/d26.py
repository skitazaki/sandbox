#!/usr/bin/env python
# -*- coding: utf-8 -*-
# removes all empty directory

import os
import os.path

def usage(program):
  print '''usage: python %s [directory..]
  ''' % (program)

def removeemptydir(root):
  for dirname, dirs, files in os.walk(root):
    """removes directory which is empty or has only one hidden file."""
    if len(dirs) == 0 and (len(files) == 0 or
        (len(files) == 1 and files[0].startswith("."))):
      answer = raw_input("remove: '%s' [y/n] " % dirname)
      if answer == "y":
        [os.unlink(os.path.join(dirname, f)) for f in files]
        os.rmdir(dirname)
        print("[INFO] removed")

if __name__ == '__main__':
  import sys
  if len(sys.argv) == 1:
    removeemptydir(os.getcwd())
  else:
    [removeemptydir(d) for d in sys.argv[1:]]

# vim: set et ts=2 sw=2 cindent fileencoding=utf-8 :

