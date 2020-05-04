#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate CREATE statements for PostgreSQL from datapackage.json.
"""

import datetime
import json
import pathlib

import click
import datapackage
import jinja2

__version__ = "0.3.0"

TEMPLATE_SQL_HEADER = """
--
-- Auto generated at {{ now.strftime('%Y/%m/%d %H:%M:%S') }}
--
-- Resources:
{% for table in tables %}--   * {{ table }}
{% endfor %}
""".strip()

TEMPLATE_SQL_CREATE = """
-- DROP TABLE IF EXISTS {{ name }} ;
CREATE TABLE IF NOT EXISTS {{ name }} (
{% for field in fields %}  "{{ field.name }}"{{ ' ' }}
  {%- if field.type == 'string' -%}
    {%- set minLength = field.constraints.get('minLength') -%}
    {%- set maxLength = field.constraints.get('maxLength') -%}
    {%- if maxLength -%}
      {%- if minLength and minLength == maxLength -%}
        CHAR({{ minLength }})
      {%- else -%}
        VARCHAR({{ maxLength }})
      {%- endif -%}
    {%- else -%}VARCHAR(100)
    {%- endif -%}
  {%- elif field.type == 'integer' %}INTEGER
  {%- elif field.type == 'boolean' %}BOOLEAN
  {%- endif -%}
  {%- if field.required %} NOT NULL{% endif -%}
  {%- if loop.nextitem is defined %},{% endif %}
{% endfor %}
) ;

{% if title %}
COMMENT ON TABLE "{{ name }}" IS '{{ title }}' ;
{% endif %}
{% for field in fields %}
{%- if field.descriptor.get('title') -%}
COMMENT ON COLUMN "{{ name }}"."{{ field.name }}" IS '{{ field.descriptor.get('title').replace("'", "''") }}' ;
{%- endif %}
{% endfor %}

{% if path -%}
-- \COPY {{ name }} FROM '{{ path }}' WITH ( FORMAT CSV, HEADER TRUE, NULL '' )
{%- endif %}
"""


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output", type=click.File("w"))
def main(input_file, output):
    """Driver function to dispatch the process."""
    path = pathlib.Path(input_file)
    click.echo(
        click.style(f"Read a datapackage: ", fg="green")
        + click.style(f"{path}", fg="green", bold=True)
    )
    package = datapackage.Package(str(path))
    header = jinja2.Template(TEMPLATE_SQL_HEADER).render(
        now=datetime.datetime.now(), tables=package.resource_names
    )
    output.write(header)
    template = jinja2.Template(TEMPLATE_SQL_CREATE)
    for r in package.resources:
        s = r.schema
        click.echo(
            click.style(f"Resource ", fg="blue")
            + click.style(f"{r.name}", fg="blue", bold=True)
            + click.style(f" has ", fg="blue")
            + click.style(f"{len(s.fields)}", fg="blue", bold=True)
            + click.style(f" fields", fg="blue")
        )
        path = None
        if r.local:
            path = r.source
        output.write(
            template.render(
                name=r.name, title=r.descriptor.get("title"), fields=s.fields, path=path
            )
        )
        output.write("\n")


if __name__ == "__main__":
    main()
