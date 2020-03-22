#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options] file1 [file2 [ ... ]]

Compose list items from a given file which is such that tweets-list.
This script is a sample program to use `jinja2` module,
which is a template engine written in Python by pocoo guys.

If you get usage of options, "-h" is a friend for you.
"""

import logging

try:
    import jinja2
except ImportError:
    raise SystemExit("`jinja2` module is not found on your system.")

from sandboxlib import parse_args, check_file_path


DEFAULT_TEMPLATE = u"""{% if texts %}
<ul>
{% for text in texts %}
<li>{{ text }}</li>
{% endfor %}
</ul>
{% else %}
<p>no "texts"</p>
{% endif %}"""


def main():
    opts, files = parse_args(doc=__doc__, postfook=check_file_path)
    if opts.filename:
        logging.info("Read template file: %s" % (opts.filename,))
        tpl = open(opts.filename).read()
    else:
        tpl = DEFAULT_TEMPLATE

    template = jinja2.Template(tpl)

    for fname in files:
        logging.info("Start to process: %s" % (fname,))
        params = {"texts": [l.strip() for l in open(fname) if l]}
        print template.render(params)

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
