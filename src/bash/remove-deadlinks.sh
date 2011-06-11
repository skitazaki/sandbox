#!/bin/sh
# Remove all dead symbolic links in a directory.
#
# <http://www.commandlinefu.com/commands/view/6939/remove-all-dead-symbolic-links-in-a-directory>

pattern=$1
dir=$2
if [ -z "$pattern" ]
then
    echo "Which pattern? 1 or 2."
    exit 1
fi
if [ -z "$dir" ]
then
    dir=.
fi

# Pattern 1.
if [ "$pattern" = "1" ]
then
    echo "Do pattern 1."
    for i in `file $dir/* | grep broken | cut -d : -f 1`
    do
        rm $i
    done
fi

# Pattern 2.
if [ "$pattern" = "2" ]
then
    echo "Do pattern 2."
    find -L $dir -type l -delete
fi
