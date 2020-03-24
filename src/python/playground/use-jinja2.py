#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sample usage of `jinja2` module.
"""

import logging
from pathlib import Path

import jinja2
from jinja2.exceptions import TemplateNotFound

from sandboxlib import parse_args

logger = logging.getLogger(Path(__file__).stem)


def setup_arguments(parser):
    parser.add_argument(
        "-d",
        "--template-dir",
        dest="template_dir",
        help="path to template directory",
        metavar="TEMPLATE_DIRECTORY",
        type=Path,
    )
    parser.add_argument(
        "-t",
        "--template",
        dest="template",
        help="path to template file",
        metavar="TEMPLATE_FILE",
        required=True,
        type=Path,
    )
    parser.add_argument(
        "files", nargs="+", help="path to variable files", metavar="FILE", type=Path,
    )


def main():
    args = parse_args(doc=__doc__, prehook=setup_arguments)
    template_dir = args.template_dir
    template_path = args.template
    files = args.files
    if template_dir is not None:
        if not template_dir.exists():
            logger.fatal(f"Template directory is not found: {template_dir}")
            exit(1)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    else:
        env = None

    if env:
        try:
            template = env.get_template(str(template_path))
        except TemplateNotFound as e:
            logger.fatal(f"Template file is not found in environment: {e}")
            exit(1)
    else:
        if not template_path.exists():
            logger.fatal(f"Template file is not found on file system: {template_path}")
            exit(1)
        logger.debug(f"Read a template file: {template_path}")
        tpl = template_path.read_text()
        template = jinja2.Template(tpl)
    for fpath in files:
        if not fpath.exists():
            logger.error(f"File not found: {fpath}")
            continue
        logger.info(f"Start rendering: {fpath}")
        with fpath.open() as fh:
            texts = [l.strip() for l in fh if l.strip()]
        print(template.render({"texts": texts}))


if __name__ == "__main__":
    main()
