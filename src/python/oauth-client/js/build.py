#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Build script to embed configuration information using Jinja2.
Specify target service defined in configuration on argument.
"""

import os.path
import ConfigParser

from twisted.python import usage

try:
    import jinja2
except ImportError:
    raise SystemExit("`jinja2` module is not found on your system.")

DEFAULT_SETTING_FILE = 'settings.ini'
OAUTH_CLIENT_HTML = 'oauth-client.html'


class Options(usage.Options):
    optParameters = [["filename", "f", DEFAULT_SETTING_FILE,
                        "Configuration file name."],
                     ["basedir", "d", '.',
                        "Directory where template files exist."]]

    def parseArgs(self, target):
        self['target'] = target


def main():
    options = Options()
    try:
        options.parseOptions()
    except usage.UsageError, errortext:
        raise SystemExit('%s, use --help' % (errortext,))

    fname = options['filename']
    basedir = options['basedir']
    target = options['target']

    if not os.path.exists(fname):
        raise SystemExit("%s is not found." % (fname,))
    parser = ConfigParser.SafeConfigParser()
    if not parser.read(fname):
        raise SystemExit("%s has no section." % (fname,))
    try:
        consumer_token = (parser.get(target, 'consumer_key'),
                          parser.get(target, 'consumer_secret'))
        if not (consumer_token[0] and consumer_token[1]):
            msg = ("No consumer token was found.",
                   "Check 'consumer_key' and 'consumer_secret' on %s." % (
                       target))
            raise SystemExit('\n'.join(msg))
        steps = [parser.get(target, 'oauth_step%d' % (i,)) for i in (1, 2, 3)]
    except ConfigParser.NoSectionError, e:
        raise SystemExit(e.message)
    except ConfigParser.NoOptionError, e:
        raise SystemExit(e.message)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(basedir))
    try:
        template = env.get_template(OAUTH_CLIENT_HTML)
    except jinja2.exceptions.TemplateNotFound, e:
        raise SystemExit("%s is not found." % (e.message,))
    params = {'hostname': target,
              'requestUrl': steps[0],
              'authorizeUrl': steps[1],
              'tokenUrl': steps[2],
              'consumerKey': consumer_token[0],
              'consumerSecret': consumer_token[1],
    }
    print template.render(params)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
