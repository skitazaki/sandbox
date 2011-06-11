#!/bin/sh
# Install ReportLab, PDF library of Python
# Usage:
# $ python=/usr/local/bin/python26 workspace=/usr/local/src sh d08.sh

python=${python-python}
program="ReportLab"
version="2_4"
workspace=${workspace-$PWD}
config=$config

site="http://www.reportlab.com/ftp"
archive_type="tar.gz"

src_dir=$PWD/$(dirname $0)
archive_util=$src_dir/extract-archive.sh

pushd $workspace
if [ $? -gt 0 ]; then
    echo "Cannot change directory to '$workspace'"
    exit 1
fi
package=${program}_$version
archive=$package.$archive_type
if [ ! -e $archive ]; then
    wget -O $archive $site/$archive
fi
if [ ! -e $package ]; then
    $archive_util $archive
fi
pushd $package
echo "Invoke with 'sudo'. Input password, please."
sudo $python setup.py install
if [ $? -gt 0 ]; then
    exit $?
fi
popd
popd

