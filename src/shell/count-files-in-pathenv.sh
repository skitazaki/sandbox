#!/bin/sh
# Count the files in each directory on your $PATH.

# 'IFS' is Internal Field Separator of shell.
IFS=:
for dir in $PATH
do
    if [ -e $dir ]
    then
        printf "%-30s: %d\n" $dir `ls -1 $dir | wc -l`
    else
        printf "%-30s: (Not found)\n" $dir
    fi
done | sort
