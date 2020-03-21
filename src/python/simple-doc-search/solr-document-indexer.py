#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creates document index on Solr.
This script assumes that source files are built with Sphinx,
and you call 'make text' at first.

Usage: %prog [options] {SOLR_SERVER_URL}
"""

import codecs
from datetime import datetime
import hashlib
import os
import sys

from solr import SolrConnection
from solr.core import utc
from twisted.python import usage
from twisted.python import log

LOCAL_SUFFIX = '.txt'


class Options(usage.Options):
    optFlags = [["verbose", "v", "verbose mode"],]
    optParameters = [
        ["basedir", "d", os.getcwd(), "base directory"],
        ["site", "s", "http://example.com", "site url to be deployed"],
        ["encoding", "e", 'utf-8', "input file encoding"],
        ["username", "u", None, "BASIC authentication user name"],
        ["password", "p", None, "BASIC authentication password"],
    ]

    def parseArgs(self, *args):
        if len(args) == 0:
            raise usage.UsageError("No argument was given.")
        if len(args) > 1:
            raise usage.UsageError("Too many arguments were given.")
        self['server'] = args[0]


def parse_document(reader):
    title = None
    while not title:
        title = reader.next().strip()
    content = ''
    for line in reader:
        s = line.strip()
        if s and not s.startswith(('**', '==', '--')):
            content += s
    return title, content


def main():
    options = Options()
    try:
        options.parseOptions()
    except usage.UsageError, errortext:
        raise SystemExit('%s, use --help' % (errortext,))

    server = options['server']
    directory = options['basedir']
    encoding = options['encoding']
    site = options['site']
    if site.endswith('/'):
        site = site[:-1]

    if not os.path.exists(directory):
        raise SystemExit('No such a directory: %s' % (directory,))

    log.startLogging(sys.stdout)
    log.msg("Document direcoty:", directory)
    log.msg("Deployed site:", site)
    log.msg("Solr server:", server)

    # Collect text documents.
    txts = []
    pos = len(directory) - 1
    for root, d, files in os.walk(directory):
        path = [os.path.join(root, f)
                for f in files if f.endswith(LOCAL_SUFFIX)]
        txts.extend(map(lambda f: \
                        (f[pos:].replace(LOCAL_SUFFIX, '.html'), f),
                        path))

    # Compose document data to store in Solr.
    documents = []
    for path, fname in txts:
        log.msg(fname, "->", path)
        url = site + path
        with codecs.open(fname, 'rb', encoding) as fp:
            title, content = parse_document(fp)
        doc = {
            'title': title,
            'content': content,
            #'last_modified': datetime.fromtimestamp(os.path.getmtime(fname)),
            'last_modified': datetime.now().replace(tzinfo=utc),
            'site': site,
            'url': url,
            'id': hashlib.sha1(url).hexdigest()
        }
        documents.append(doc)
    u = options['username']
    p = options['password']
    if u and p:
        s = SolrConnection(server, http_user=u, http_pass=p)
    else:
        s = SolrConnection(server)
    s.add_many(documents)
    s.commit()

if __name__ == '__main__':
    main()

