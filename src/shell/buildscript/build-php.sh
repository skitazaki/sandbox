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
archive_util=$src_dir/extract-archive.sh
tmp_file="/tmp/`basename $0`.txt"
echo "Just Do It:" >$tmp_file

pushd $workspace
for v in $@; do
    major=${v:0:1}
    minor=${v:2:1}
    package=$program-$v
    archive=$package.$archive_type
    [ -f $archive ] ||
        wget -O $archive $site/$archive/from/$mirror
    [ $? -eq 0 ] || exit $?
    [ -d $package ] || $archive_util $archive
    prefix="/usr/local/$package"
    pushd $package
    ./configure --prefix=$prefix $config && make
    [ $? -eq 0 ] || exit $?
    cat >>$tmp_file <<EOT
    pushd $PWD && sudo make install && popd
    sudo ln -s $prefix/bin/php $bin_dir/$program$major$minor
EOT
    popd
done
popd

cat <<EOT
########################################
Install them and create symbolic link!!
`cat $tmp_file`
########################################
EOT
rm $tmp_file
