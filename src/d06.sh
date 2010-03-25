#!/bin/sh
# Build PHP from source package
# Usage:
# $ program=php workspace=/usr/local/src sh d06.sh 5.2.13 5.3.2
# $ workspace=/usr/local/src config="--with-pdo-mysql=mysqlnd" \\
#             sh src/d06.sh 5.3.2

if [ $# -lt 1 ]; then
    echo "Usage:"
    echo "$0 version [version...]"
    exit 1
fi

program=${program-php}
workspace=${workspace-$PWD}
bin_dir=${bin_dir-/usr/local/bin}
config=$config

site="http://jp.php.net/get"
archive_type="tar.bz2"

src_dir=$PWD/$(dirname $0)
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
        wget -O $archive $site/$archive/from/jp.php.net/mirror
    fi
    if [ ! -e $package ]; then
        $archive_util $archive
    fi
    prefix="/usr/local/$package"
    pushd $package
    ./configure --prefix=$prefix $config && make
    if [ $? -gt 0 ]; then
        exit $?
    fi
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
