#!/usr/bin/env python
# -*- coding: utf-8 -*-
# fetches titles from IMAP server in INBOX
# example:
# python d23.py -f d23.json

import getopt
import getpass
import imaplib
import json
import sys

def usage(program):
  print '''usage: python %s -f settingfile
  setting file is a JSON.
  ''' % (program)
  sys.exit(1)

def fetchtitles(info):
  try:
    if info.has_key('ssl'):
      mail = imaplib.IMAP4_SSL(info.get('host'), info.get('port', 993))
    else:
      mail = imaplib.IMAP4(info.get('host'), info.get('port', 143))
  except IOError:
    raise IOError("could not connect: %s:%s" %
            (info.get('host'), info.get('port')))
  print("connect as '%s' on '%s'" % (info.get('user'), info.get('host')))
  try:
    mail.login(info.get('user'), getpass.getpass())
  except IOError:
    raise IOError("reject to login: %s" % info.get('user'))
  ret, l = mail.list()
  if ret == "OK":
    print("available mailboxes are:")
    print(" - " + ("\n - ".join([b for b in l])))
  print("select INBOX")
  mail.select("INBOX")
  typ, data = mail.search(None, "ALL")
  for num in data[0].split():
    typ, body = mail.fetch(num, "(BODY[HEADER.FIELDS (SUBJECT)])")
    print("Message %s:\n%s" % (num, body[0][1].strip()))
  mail.close()
  mail.logout()

if __name__ == '__main__':
  try:
    opts, args = getopt.getopt(sys.argv[1:], "f:")
  except getopt.GetoptError:
    usage(sys.argv[0])
  for o,v in opts:
    if o == "-f":
      fname = v
    else:
      pass
  try:
    info = json.load(open(fname))
  except NameError:
    print("use -f option to specify setting file.")
    sys.exit(1)
  except IOError:
    print("could not found: %s" % fname)
    sys.exit(1)
  try:
    fetchtitles(info)
  except IOError, e:
    print(e)

# vim: set et ts=2 sw=2 cindent fileencoding=utf-8 :

