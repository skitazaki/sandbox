#!/bin/sh
PATH_SEPARATOR=":"

for dir in `echo $PATH | sed "s/$PATH_SEPARATOR/ /g"`
do
    if [ -e $dir ]
    then
        printf "%-30s: %d\n" $dir `ls -1 $dir | wc -l`
    else
        printf "%-30s: (Not found)\n" $dir
    fi
done | sort
