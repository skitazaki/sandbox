#!/usr/bin/env python
__doc__ = """\
nosetests d70.py

simple test using `nose` and raise ``AssertionError`` intentionally.
"""

import os

def test_script_exists():
    """This test intentionally fails"""
    assert os.path.exists("notfound.csv")

