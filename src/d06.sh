#!/bin/sh
# Build PHP from source package
# example:
# $ PROGRAM=php WORKSPACE=/usr/local/src sh d06.sh 5.2.13 5.3.2
# $ WORKSPACE=/usr/local/src CONFIG="--with-pdo-mysql=mysqlnd" \\
#             sh d06.sh 5.3.2

if [ $# -lt 1 ]; then
    cat <<EOT
usage: sh $0 version [version...]
EOT
    exit 1
fi

# file specific settings
site="http://jp.php.net/get"
mirror="jp.php.net/mirror"
archive_type="tar.bz2"

# general build script settings
program=${PROGRAM-php}
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
    package=$program-$v
    archive=$package.$archive_type
    if [ ! -e $archive ]; then
        wget -O $archive $site/$archive/from/$mirror
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
    sudo ln -s $prefix/bin/php $bin_dir/$program$major$minor
EOT
    popd
done
popd

echo "########################################"
echo "Install them and create symbolic link!!"
cat $tmp_file
echo "########################################"

rm $tmp_file
