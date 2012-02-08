#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""python %prog [options] file1 [file2 [ ... ]]

Use "template inheritance" feature provided by jinja2.
This is similar to Django's one.
"""

import codecs
import logging
import os

try:
    import jinja2
except ImportError:
    raise SystemExit("`jinja2` module is not found on your system.")

from sandboxlib import parse_args, check_file_path

DEFAUT_BUILD_DIR = "_build"


def main():
    opts, files = parse_args(doc=__doc__, minargc=1)
    outdir = opts.output or DEFAUT_BUILD_DIR
    if not os.path.exists(outdir):
        os.mkdir(outdir)
        logging.info("Created %s", outdir)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(opts.basedir))

    for fname in files:
        logging.info("Start to process: %s", fname)
        template = env.get_template(fname)
        out = os.path.join(outdir, fname)
        with codecs.open(out, "wb", encoding=opts.enc_out) as w:
            w.write(template.render())
        logging.info("Wrote to %s", out)


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
