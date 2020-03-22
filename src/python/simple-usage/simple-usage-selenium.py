#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample usage of Selenium with Python client.

See `Python bindings of Python
<http://pypi.python.org/pypi/selenium>`_ on pypi.

Try it out with `nose` after running selenium-server. ::

    $ nosetests d83
"""
from selenium.remote import connect
from selenium import CHROME
from selenium.common.exceptions import NoSuchElementException
from time import sleep

browser = connect(CHROME)  # Get local session of Google Chrome
browser.get("http://www.google.co.jp")  # Load page
assert browser.get_title() == "Google"
elem = browser.find_element_by_name("q")  # Find the query box
elem.send_keys("selenium")
browser.find_element_by_name("btnG").click()
sleep(0.2)  # Let the page load, will be added to the API
try:
    browser.find_element_by_xpath(
            """//a[contains(@href,"http://seleniumhq.org")]""")
except NoSuchElementException:
    assert 0, "can't find seleniumhq on search result."
browser.close()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
