#!/bin/sh
# Build Python from source package
# Usage:
# $ workspace=/usr/local/src sh d05.sh 2.6.5 3.1.2

if [ $# -lt 1 ]; then
    echo "Usage:"
    echo "$0 version [version...]"
    exit 1
fi

workspace=${workspace-$PWD}
bin_dir=${bin_dir-/usr/local/bin}
src_dir=$PWD/$(dirname $0)
archive_util=$src_dir/d04.sh
tmp_file="$src_dir/d05.txt"
echo "Just Do It:" >$tmp_file

archive_type="tar.bz2"
python_site="http://www.python.org/ftp/python"
python_config=

pushd $workspace
for v in $@; do
    major=${v:0:1}
    minor=${v:2:1}
    python_version=$v
    python_package="Python-$python_version"
    if [ ! -e $python_package.$archive_type ]; then
        wget $python_site/$python_version/$python_package.$archive_type
    fi
    if [ ! -e $python_package ]; then
        $archive_util $python_package.$archive_type
    fi
    prefix="/usr/local/$python_package"
    pushd $python_package
    ./configure --prefix=$prefix $python_config && make
    if [ $major == "3" ]; then
        bin="python3"
    else
        bin="python"
    fi
    cat >>$tmp_file <<EOT
    pushd $PWD && sudo make install && popd
    sudo ln -s $prefix/bin/$bin $bin_dir/python$major$minor
EOT
    popd
done
popd

echo "########################################"
echo "Install them and create symbolic link!!"
cat $tmp_file
echo "########################################"

rm $tmp_file
