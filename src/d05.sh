#!/bin/sh
# Build Python from source package
# example:
# $ WORKSPACE=/usr/local/src sh d05.sh 2.6.5 3.1.2

if [ $# -lt 1 ]; then
    cat <<EOT
usage: sh $0 version [version...]
EOT
    exit 1
fi

# file specific settings
site="http://www.python.org/ftp/python"
archive_type="tar.bz2"

# general build script settings
program=${PROGRAM-python}
workspace=${WORKSPACE-$PWD}
bin_dir=${BINDIR-/usr/local/bin}
config=$CONFIG

# utility
src_dir=`cd $(dirname $0) && pwd`
archive_util=$src_dir/d04.sh
tmp_file="/tmp/`basename $0`.txt"
echo "Just Do It:" >$tmp_file

pushd $workspace
for v in $@; do
    major=${v:0:1}
    minor=${v:2:1}
    package="Python-$v"
    archive=$package.$archive_type
    if [ ! -e $archive ]; then
        wget -O $archive $site/$v/$archive
        if [ $? -gt 0 ]; then exit $?; fi
    fi
    if [ ! -e $package ]; then
        $archive_util $archive
    fi
    prefix="/usr/local/$package"
    pushd $package
    ./configure --prefix=$prefix $config && make
    if [ $? -gt 0 ]; then exit $?; fi
    if [ $major == "3" ]; then
        bin="python3"
    else
        bin="python"
    fi
    cat >>$tmp_file <<EOT
    pushd $PWD && sudo make install && popd
    sudo ln -s $prefix/bin/$bin $bin_dir/$program$major$minor
EOT
    popd
done
popd

echo "########################################"
echo "Install them and create symbolic link!!"
cat $tmp_file
echo "########################################"

rm $tmp_file
