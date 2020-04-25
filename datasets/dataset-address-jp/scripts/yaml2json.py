#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Convert datapackage file format from YAML to JSON.
"""

import json
import pathlib

import yaml

__version__ = "0.4.0"

SCRIPT_PATH = pathlib.Path(__file__)
BASEDIR = SCRIPT_PATH.parent.parent.resolve()

DATAPACKAGE_NAME = "datapackage.json"
DATAPACKAGE_PATH = BASEDIR / DATAPACKAGE_NAME

DATAPACKAGE_SOURCE_NAME = "datapackage.yaml"
DATAPACKAGE_SOURCE_PATH = BASEDIR / DATAPACKAGE_SOURCE_NAME


def main():
    """Driver function to dispatch the process."""
    source = yaml.safe_load(DATAPACKAGE_SOURCE_PATH.open())
    output = DATAPACKAGE_PATH.open("w")
    json.dump(source, output, indent=2, sort_keys=True, ensure_ascii=False)
    output.close()


if __name__ == "__main__":
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
