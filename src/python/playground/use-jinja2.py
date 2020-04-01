# -*- coding: utf-8 -*-

"""Sample usage of `jinja2` module.
"""

import logging
from pathlib import Path

import click
import jinja2
from jinja2.exceptions import TemplateNotFound

from sandboxlib import main

logger = logging.getLogger("sandbox")


@main.command("run")
@click.option(
    "-d",
    "--template-dir",
    type=click.Path(exists=True),
    help="path to template directory",
)
@click.option("-t", "--template-name", help="name of template file", required=True)
@click.argument("file", type=click.File("r"), nargs=-1)
def run(template_dir, template_name, file):
    if template_dir is None:
        template_path = Path(template_name)
        if not template_path.exists():
            logger.fatal(f"Template file is not found on file system: {template_path}")
            return
        logger.debug(f"Read a template file: {template_path}")
        tpl = template_path.read_text()
        template = jinja2.Template(tpl)
    else:
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        try:
            template = env.get_template(template_name)
        except TemplateNotFound as e:
            logger.fatal(f"Template file is not found in environment: {e}")
            return

    for fh in file:
        logger.info(f"Start rendering with: {fh.name}")
        texts = [l.strip() for l in fh.readlines() if l.strip()]
        print(template.render({"texts": texts}))


if __name__ == "__main__":
    main()
