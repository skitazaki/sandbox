#!/bin/sh

# Extract zipped archive, 'tar.gz', 'tgz', 'tar.bz2', and 'zip'.

if [ $# -lt 1 ]; then
    echo "Usage:"
    echo "$0 archive [archive...]"
    exit 1
fi

for f in $*; do
    case $f in
    *.tar.gz)
        tar xzf $f
        ;;
    *.tgz)
        tar xzf $f
        ;;
    *.tar.bz2)
        tar xjf $f
        ;;
    *.zip)
        unzip $f
        ;;
    *)
        ;;
    esac
done

