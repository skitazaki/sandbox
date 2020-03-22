#!/bin/sh
# Create a project using autotools.
#
# <http://www.spa.is.uec.ac.jp/~kinuko/slidemaker/autotools/>
# <http://module.jp/blog/autotoolize_spidermonkey.html>

DEVELOPER_NAME="YOUR_NAME"
DEVELOPER_EMAIL="you@example.com"

project=$1
mainfile=$project.cpp

die() { echo $1; exit 1; }
[ -z $project ] && die "specify project name."
[ -d $project ] && die "project \"$project\" already exists."

# check autotools are installed.
autoscan --version >/dev/null;   [ $? -eq 0 ] || exit 1
aclocal --version >/dev/null;    [ $? -eq 0 ] || exit 1
automake --version >/dev/null;   [ $? -eq 0 ] || exit 1
autoheader --version >/dev/null; [ $? -eq 0 ] || exit 1
automake --version >/dev/null;   [ $? -eq 0 ] || exit 1

currentdir=`pwd`
mkdir $project; cd $project

cat <<EOF >Makefile.am
bin_PROGRAMS = $project
${project}_SOURCES = src/$mainfile

MAINTAINERCLEANFILES = *~
EOF

mkdir src
cat <<EOF >src/$mainfile
#include <iostream>

int main(int argc, char* argv[])
{
    std::cout << "Hello $project" << std::endl;
    std::cout << __FILE__ << " " << __DATE__ << " " << __TIME__ << std::endl;
    std::cout << "char:   " << sizeof(char) << std::endl;
    std::cout << "int:    " << sizeof(int) << std::endl;
    std::cout << "long:   " << sizeof(long) << std::endl;
    std::cout << "double: " << sizeof(double) << std::endl;
    std::cout << "float:  " << sizeof(float) << std::endl;
    return 0;
}
EOF

autoscan
sed -e s/FULL-PACKAGE-NAME/$project/ -e s/VERSION/0.1/ \
    -e s/BUG-REPORT-ADDRESS/$DEVELOPER_EMAIL/ configure.scan |
  awk '{ print $0 }
    substr($0, 0, 7) == "AC_INIT" { print "AM_INIT_AUTOMAKE" }' >configure.in
touch NEWS README ChangeLog
echo "$DEVELOPER_NAME <$DEVELOPER_EMAIL>" >AUTHORS
aclocal
autoheader
automake -a -c
autoconf

./configure
make
echo "**********************************************************************"
./$project

cd $currentdir
