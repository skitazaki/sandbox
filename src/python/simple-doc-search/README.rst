================================
Simple document search with Solr
================================

Requirements
============
* Python 2.7
    * `virtualenv`

*Mac OSX Lion* is recommended.

Setup
=====
First, setup your Python development environment with `virtualenv` and `waf`. ::

    $ virtualenv --distribute .
    $ source bin/activate
    $ curl http://waf.googlecode.com/files/waf-1.6.11 >bin/waf
    $ chmod +x bin/waf

Second, download Solr distribution package and place it somewhere. ::

    $ waf configure build

Dotclond instances
==================
Create `dotcloud` instances. ::

    $ dotcloud create docsearch

Push Solr configuration files. ::

    $ dotcloud push docsearch solr

And, get servers' information. ::

    $ waf dotcloud_info

Implement / Test
================
Start Solr test server with custom configuration. ::

    $ waf run_solr &

Run test suite. ::

    $ waf test

Frontend sample code is under 'static' directory.

About
=====
KITAZAKI Shigeru

