#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""\
Sample test suite using `selenium` module.

This script try to login Google.

NOTICE:
selenium-2.0a5 has a bug to call `base64.decodestring`. you MUST fix it
before running this.

A side note about capturing screen shot using Python.
<http://kshigeru.blogspot.com/2011/02/screen-capture-using-python.html>
"""

import getpass
import time
import unittest

from selenium.remote import connect
from selenium import CHROME
from selenium.common.exceptions import NoSuchElementException

HOST = 'http://google.com'
print 'Connect to %s' % (HOST,)

TEST_USER = []
username = getpass.getpass('Username> ')
if username:
    TEST_USER.append(username)
else:
    sys.exit(1)
password = getpass.getpass('Password> ')
if password:
    TEST_USER.append(password)
else:
    sys.exit(1)

BROWSER = connect(CHROME)


def load(path):
    BROWSER.get(HOST + path)
    return BROWSER


class WebServiceTest(unittest.TestCase):

    def setUp(self):
        browser = load('/')
        # Move login page.
        try:
            browser.find_element_by_id('gb_70').click()
        except NoSuchElementException:
            return
        # Find the login form and fill it.
        try:
            form = browser.find_element_by_id('gaia_loginform')
            form.find_element_by_name('Email').send_keys(TEST_USER[0])
            form.find_element_by_name("Passwd").send_keys(TEST_USER[1])
            form.submit()
            time.sleep(3)
        except NoSuchElementException:
            pass

    def tearDown(self):
        pass

    def test_A(self):
        browser = load('/')
        menu = browser.find_element_by_class_name('gb1')
        assert menu
        # do nothing cause this is not anchor.
        menu.click()
        time.sleep(5)
        browser.get_screenshot_as_file('screen_A.png')

    def test_B(self):
        browser = load('/')
        menu = browser.find_elements_by_class_name('gb1')
        assert len(menu) > 2
        # Video.
        menu[2].click()
        time.sleep(5)
        browser.get_screenshot_as_file('screen_B.png')

    def test_C(self):
        browser = load('/')
        menu = browser.find_elements_by_class_name('gb4')
        assert menu
        # iGoogle.
        menu[1].click()
        time.sleep(5)
        browser.get_screenshot_as_file('screen_C.png')

if __name__ == '__main__':
    unittest.main()

BROWSER.quit()

# vim: set expandtab tabstop=4 shiftwidth=4 cindent :
