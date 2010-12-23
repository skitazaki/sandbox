#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample usage of `twisted.web.html
<http://twistedmatrix.com/trac/browser/tags/releases/twisted-10.1.0/twisted/web/html.py>`_.

If you run doctest, give `test` on first argument.
"""

import twisted.web.html

def plain_list():
    """
    >>> plain_list()
    <ul>
    <li> one</li>
    <li> 2</li>
    <li> さん</li>
    <li> True</li>
    <li> None</li>
    </ul>
    """
    data = ["one", 2, "さん", True, None]
    print twisted.web.html.UL(data)

def anchor_list():
    """
    >>> anchor_list()
    <ul>
    <li> <a href="http://google.com">Google</a></li>
    <li> <a href="http://yahoo.com">Yahoo!</a></li>
    <li> <a href="http://microsoft.com">Microsoft</a></li>
    </ul>
    """
    data = [("http://google.com", "Google"),
            ("http://yahoo.com", "Yahoo!"),
            ("http://microsoft.com", "Microsoft")]
    print twisted.web.html.linkList(data)

def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        import doctest
        doctest.testmod()
    else:
        plain_list()
        anchor_list()

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :

