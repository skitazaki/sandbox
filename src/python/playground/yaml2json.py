# -*- coding: utf-8 -*-

"""Convert data from YAML to JSON.
"""

import logging
import json

import yaml

from sandboxlib import parse_args, setup_fileio, check_file_path


def yaml2json(fname):
    try:
        cfg = yaml.safe_load(open(fname))
        print(json.dumps(cfg, indent=2))
    except Exception:
        logging.error(f"Invalid YAML file: {fname}")


def main():
    args = parse_args(doc=__doc__, prehook=setup_fileio, posthook=check_file_path)
    files = args.files
    for fname in files:
        yaml2json(fname)


if __name__ == "__main__":
    main()
