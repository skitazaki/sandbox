#!/bin/sh
# Install MySQLdb.
#   you need 'mysql_config' on your machine.
# example:
# $ PYTHON=/usr/local/bin/python26 WORKSPACE=/usr/local/src \
#     MYSQL_CONFIG=/usr/local/mariadb-5.1.44/bin/mysql_config sh d25.sh

myconfig=${MYSQL_CONFIG-mysql_config}
$myconfig --version >/dev/null 2>&1
if [ $? -gt 0 ]
then
    echo "'mysql_config' is required in your PATH."
    exit 1
fi
# file specific settings
site="http://sourceforge.net/projects/mysql-python/files/mysql-python-test"
archive_type="tar.gz"
program="MySQL-python"
version="1.2.3c1"
python=${PYTHON-python}

# general build script settings
workspace=${WORKSPACE-$PWD}
bin_dir=${BINDIR-/usr/local/bin}
config=$CONFIG

# utility
src_dir=`cd $(dirname $0) && pwd`
archive_util=$src_dir/extract-archive.sh

pushd $workspace
if [ $? -gt 0 ]; then
    echo "Cannot change directory to '$workspace'"
    exit 1
fi
package=${program}-$version
archive=$package.$archive_type
[ -f $archive ] ||
    wget -O $archive $site/$version/$archive/download
[ $? -eq 0 ] || exit $?
[ -d $package ] || $archive_util $archive
pushd $package
# for setup tools
$python -c 'import setuptools' >/dev/null 2>&1
[ $? -eq 0 ] || sudo $python ez_setup.py
# if 'mysql_config' is not in PATH, add custom value in 'site.cfg'
mysql_config --version >/dev/null 2>&1
[ $? -eq 0 ] || echo "mysql_config = $myconfig" >>site.cfg
$python setup.py build
if [ $? -gt 0 ]; then exit $?; fi
cat <<EOT
############################################################
Install them and test it!!
  pushd $PWD && sudo $python setup.py install && popd
  $python -c 'import MySQLdb'
############################################################
EOT
popd; popd

