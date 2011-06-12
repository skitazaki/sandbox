#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """\
python %prog [options] file [,file ...]

Compose list items from a given file which is such that tweets-list.
This script is a sample program to use `jinja2` module, which is a template
engine written in Python by pocoo guys.

If you get usage of options, "-h" is a friend for you.
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
    parser.add_option("-t", "--template", dest="template",
            default="d73.html", metavar="FILE", help="template file")

    opts, args = parser.parse_args()

    if not args:
        parser.error("no parsing file is specified.")

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)

    return opts.template, args


def main():
    template_file, target_files = parse_args()

    if not os.path.exists(template_file):
        logging.fatal("%s is not found." % (template_file,))
        sys.exit(1)

    logging.debug("read template file: %s" % (template_file,))
    template = jinja2.Template(open(template_file).read())

    for file in target_files:
        if not os.path.exists(file):
            logging.error("%s is not found." % (file,))
            continue

        logging.info("start to process: %s" % (file,))

        params = {"texts": [l.strip() for l in open(file)]}
        sys.stdout.write(template.render(params))

if __name__ == "__main__":
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
