#!/bin/sh
# -*- coding: utf-8 -*-
#
# Run `pep8` and `nosetests` for given scripts.

files=$*

[ -n "$files" ] || files=`ls *.py`

echo "Target files are:"
line=""
for f in $files
do
    line="$line $f"
    if [ ${#line} -gt 80 ]
    then
        echo $line
        line=""
    fi
done

echo
echo "Check PEP-8 style."
pep8 $files

echo
echo "Run tests of files."

for f in $files
do
    nosetests $f
    [ $? == 0 ] || echo $f >>error
    c=${f%%.py}.pyc
    [ -f $c ] && rm $c
done

echo "See \`error\` file."

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :

