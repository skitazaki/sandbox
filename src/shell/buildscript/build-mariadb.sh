#!/bin/sh
# Build MariaDB from source package
# example:
# $ PROGRAM=mariadb WORKSPACE=/usr/local/src sh d12.sh 5.1.44

if [ -z $PROGRAM ]; then
    echo "set 'PROGRAM'."
    exit 1
fi
if [ $# -lt 1 ]; then
    cat <<EOT
This is a simple build script of MariaDB.

usage: PROGRAM=mariadb sh $0 version [version...]

options: set by environment variables.
  PROGRAM (mandatory)
    - program name such as 'mariadb'
  WORKSPACE (default:\$PWD=$PWD)
    - directory where packages are downloaded
  BINDIR (default:/usr/local/bin)
    - directory to suggest create a symbolic link of program file
  CONFIG
    - build option passing to 'configure' script
EOT
    exit 0
fi

# file specific settings
site="http://askmonty.org/downloads"
mirror="http://maria.llarian.net/download"
aux="distro/kvm-tarbake-jaunty-x86"
archive_type="tar.gz"

# general build script settings
program=${PROGRAM}
workspace=${WORKSPACE-$PWD}
bin_dir=${BINDIR-/usr/local/bin}
config=$CONFIG

# utility
src_dir=`cd $(dirname $0) && pwd`
archive_util=$src_dir/extract-archive.sh
tmp_file="/tmp/`basename $0`.txt"
echo "Just Do It:" >$tmp_file

pushd $workspace
for v in $@; do
    major=${v:0:1}
    minor=${v:2:1}
    package=$program-$v
    archive=$package.$archive_type
    if [ ! -e $archive ]; then
        wget -O $archive $site/r/$mirror/$package/$aux/$archive
        if [ $? -gt 0 ]; then exit $?; fi
    fi
    if [ ! -e $package ]; then
        $archive_util $archive
    fi
    prefix="/usr/local/$package"
    pushd $package
    ./configure --prefix=$prefix $config && make
    if [ $? -gt 0 ]; then exit $?; fi
    cat >>$tmp_file <<EOT
    pushd $PWD && sudo make install && popd
    #sudo ln -s $prefix/bin/$program $bin_dir/$program$major$minor
    sudo $PWD/bin/mysql_install_db --basedir=$PWD --datadir=$PWD/data
EOT
    popd
done
popd

echo "########################################"
echo "Install them and create symbolic link!!"
cat $tmp_file
echo "########################################"

rm $tmp_file

