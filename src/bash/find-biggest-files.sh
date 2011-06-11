#!/bin/sh
# -*- coding: utf-8 -*-
#
# Find the 10 biggest files taking disk spaces.
# <http://www.commandlinefu.com/commands/view/6993>

target=${1-$PWD}

echo "Target directory: $target"

find $target -type f |xargs du 2>/dev/null |
    sort -nr |head -10 |
    xargs -n 1 du -h 2>/dev/null

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :