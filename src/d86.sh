#!/bin/sh
#
# Copy PNG image files of HTML assets.
#

dest=$1
targets="part15 part16 part17 part18 part19 part20 part21 part22"

[ -z "$dest" ] &&
    echo "No destination, please give me a directory path." && exit 1

[ ! -d "$dest" ] &&
    echo "$dest is not found." && exit 1

for t in $targets
do
    for p in `ls ${t}_files/*.png`
    do
        f=`basename $p`
        cp $p $dest/${t}_$f
        chmod -x $dest/${t}_$f
    done
done

