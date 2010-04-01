#!/bin/sh
# Stage files which are not version-controlled on Subversion.
# except: mime type is application/octet-stream or application/x-archive

dir=${1-.}
for f in `svn st $dir | grep -v ${0#./} |awk '$1 == "?" { print $2; }'`
do
    if [ -f $f ]; then
        type=`file --mime $f |cut -d: -f2 |sed 's/[[:space:]]//'`
        if [ $type == "application/octet-stream" -o \
             $type == "application/x-archive" ]; then
             echo "$f is a binary file."
        else
            svn add $f;
        fi
    fi
done

