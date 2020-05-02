#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Convert datapackage file format from YAML to JSON.
"""

import json
import pathlib

import click
import yaml

__version__ = "0.4.0"


@click.command()
@click.option("--output-file", type=click.Path())
@click.argument("input_file", type=click.Path(exists=True))
def main(input_file, output_file):
    """Driver function to dispatch the process."""
    path = pathlib.Path(input_file)
    if output_file is None:
        output_path = path.with_suffix(".json")
    else:
        output_path = pathlib.Path(click.format_filename(output_file))
    click.secho(f"Read a YAML file: {path}")
    try:
        contents = yaml.safe_load(path.open())
    except Exception as e:
        click.secho(f"Invalid YAML file: {e}", fg="red")
        raise click.Abort()
    if output_path.exists():
        click.secho(f"Overwrite a JSON file: {output_path}", fg="magenta")
    else:
        click.secho(f"Produce a JSON file: {output_path}", fg="green")
    with output_path.open("w") as fp:
        json.dump(contents, fp, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    main()
