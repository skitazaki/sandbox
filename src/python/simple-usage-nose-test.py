#!/usr/bin/env python

"""nosetests %prog

Simple test using `nose` and raise ``AssertionError`` intentionally.
"""

import os


def test_script_exists():
    """This test intentionally fails"""
    assert os.path.exists("notfound.csv")

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
