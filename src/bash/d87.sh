#!/bin/sh
#
# Serve contents in current directory via HTTP by Python.
#

python=${1-python}

version=`$python -c "import sys; sys.stdout.write(str(sys.version_info[0]))"`
[ $? -gt 0 ] && exit $?

echo "Your interpreter major version is $version."

case "$version" in
2)
    $python -m SimpleHTTPServer &
    sleep 2
    ps
    ;;
3)
    $python -m http.server &
    sleep 2
    ps
    ;;
*)
    echo "Unknown version. $version"
    exit 1
    ;;
esac

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
