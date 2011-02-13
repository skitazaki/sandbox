#!/bin/sh
# Install PIL, Python Image Library
# example:
# $ PYTHON=/usr/local/bin/python26 WORKSPACE=/usr/local/src sh d13.sh

# file specific settings
site="http://effbot.org/downloads"
archive_type="tar.gz"
program="Imaging"
version="1.1.7"
python=${PYTHON-python}

# general build script settings
workspace=${WORKSPACE-$PWD}
bin_dir=${BINDIR-/usr/local/bin}
config=$CONFIG

# utility
src_dir=`cd $(dirname $0) && pwd`
archive_util=$src_dir/d04.sh

pushd $workspace
if [ $? -gt 0 ]; then
    echo "Cannot change directory to '$workspace'"
    exit 1
fi
package=${program}-$version
archive=$package.$archive_type
if [ ! -e $archive ]; then
    wget -O $archive $site/$archive
    if [ $? -gt 0 ]; then exit $?; fi
fi
if [ ! -e $package ]; then
    $archive_util $archive
fi
pushd $package
$python setup.py build
if [ $? -gt 0 ]; then exit $?; fi
echo "########################################"
echo "Install them and test it!!"
echo "pushd $PWD && sudo $python setup.py install && popd"
echo "$python -c 'import Image'"
echo "########################################"
popd; popd

