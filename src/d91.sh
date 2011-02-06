#!/bin/sh
# Counts of commit per commiters.
#
# see `Top SVN committers
# <http://www.commandlinefu.com/commands/view/7545/top-svn-committers-without-awk>`.
# see `d20.sh`

dir=${1-.}

svn log -q $dir | grep '^r[0-9]' | cut -f2 -d "|" | sort | uniq -c | sort -nr

