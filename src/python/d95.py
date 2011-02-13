#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """\
python %prog [options] file [,file ...]

Use "template inheritance" feature provided by jinja2.
This is similar to Django's one.
"""

import logging
import optparse
import os.path
import sys

try:
    import jinja2
except ImportError:
    logging.fatal("`jinja2` module is not found on your system.")
    sys.exit(1)


def parse_args():
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-v", "--verbose", dest="verbose",
            default=False, action="store_true", help="verbose mode")
    parser.add_option("-q", "--quiet", dest="verbose",
            default=True, action="store_false", help="quiet mode")

    opts, args = parser.parse_args()

    if not args:
        parser.error("no parsing file is specified.")

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)

    return args


def main():
    files = parse_args()

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))

    for file in files:
        if not os.path.exists(file):
            logging.error("%s is not found." % (file,))
            continue

        logging.info("start to process: %s" % (file,))
        writer = sys.stdout

        template = env.get_template(file)
        writer.write(template.render())


def test():
    base = '{% extends "base.html" %}'
    tests = {
        'base.html': "BA{% block title %}{% endblock %}SE",
        'test1.html': base + "{% block title %}1{% endblock %}",
        'test2.html': base + "{% block title %}2{% endblock %}"
    }
    env = jinja2.Environment(loader=jinja2.DictLoader(tests))
    tpl = env.get_template('test1.html')
    ret = tpl.render()
    logging.debug(ret)
    assert ret == 'BA1SE'
    tpl = env.get_template('test2.html')
    ret = tpl.render()
    logging.debug(ret)
    assert ret == 'BA2SE'

if __name__ == "__main__":
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
