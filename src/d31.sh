#!/bin/sh
# splits patch files into each file
# example:
# $ sh d31.sh *.patch

for file in $*
do
    base=`basename ${file%%.patch}`
    cat $file |
    awk '$1 == "diff" { file = $NF; gsub("/", "_", file) }
         $1 == "--" { file = "" }
         file != "" {
             output = sprintf("'$base'-%s.patch", file);
             print $0 >> output
         }'
done

