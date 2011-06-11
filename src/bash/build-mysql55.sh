#!/bin/sh
#
# Build MySQL 5.5 from a source package.
# We must download source package prior to run script because Oracle requires
# login form on his Web site.
#
# Notice that MySQL uses `CMake` on build system since version 5.5.
# See also `INSTALL-SOURCE` in the source package.
#
# Similar script is available as `d12.sh`, which builds mariadb-5.1 series.
# Of course, that uses `configure` not `cmake` yet.
#
# Example:
# $ WORKSPACE=/usr/local/src VERSION=5.5.8 sh d88.sh
#

PROGRAM=mysql
VERSION=${VERSION-5.5.8}
DAEMON_USER=mysql
DAEMON_GROUP=mysql

if [ -z "$VERSION" ]; then
    cat <<EOT
This is a simple build script of MySQL 5.5.

usage: sh $0 [CMAKE-CONFIGURE-OPTIONS]

options: set by environment variables.
  VERSION (mandatory)
    - program source code version to download.
  WORKSPACE (default:\$PWD=$PWD)
    - directory where packages are downloaded.
  BINDIR (default:/usr/local/bin)
    - directory to suggest create a symbolic link of program file.
EOT
    exit 0
fi

# File specific settings.
archive_type="tar.gz"

echo "User and Group entity as daemon."
[ -f /etc/passwd ] && grep $DAEMON_USER /etc/passwd
[ -f /etc/group ] && grep $DAEMON_GROUP /etc/group

# General build script settings.
program=${PROGRAM}
workspace=${WORKSPACE-$PWD}
bin_dir=${BINDIR-/usr/local/bin}
config=$*

package=$program-$VERSION
archive=$package.$archive_type

# Utility
src_dir=`cd $(dirname $0) && pwd`
archive_util=$src_dir/extract-archive.sh
tmp_file="/tmp/`basename $0`.txt"

# Start build.
pushd $workspace
if [ ! -f $archive ]
then
    echo "$archive archive not found on your working directory."
    exit 1
fi
if [ ! -e $package ]
then
    echo "Extract $archive."
    $archive_util $archive
fi

prefix="/usr/local/$package"
pushd $package

cmake . \
    -DCMAKE_INSTALL_PREFIX=$prefix \
    -DWITH_INNOBASE_STORAGE_ENGINE=1 \
    -DDEFAULT_CHARSET=utf8mb4 $config
make
[ $? -gt 0 ] && exit $?

# Postinstallation setup followed on `INSTALL-SOURCE`.
cat <<EOT >$tmp_file
pushd $PWD && sudo make install && popd
sudo ln -s $prefix/bin/$program $bin_dir/$program-$VERSION
sudo chown -R $DAEMON_USER $prefix
sudo chgrp -R $DAEMON_GROUP $prefix
sudo $prefix/scripts/mysql_install_db --basedir=$prefix \
    --datadir=$prefix/data --user=$DAEMON_USER
sudo cp $PWD/support-files/my-medium.cnf /etc/my.cnf #optional
sudo cp $PWD/support-files/mysql.server /etc/init.d/mysql.server # Optional
sudo $prefix/bin/mysqld_safe --user=$DAEMON_USER &
EOT
popd
popd

echo "########################################"
echo "Install them and create symbolic link!!"
cat $tmp_file
echo "########################################"

rm $tmp_file

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
