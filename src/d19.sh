#!/bin/sh
# switches java version on MacOSX.
# example
# $ VERSION=1.6 sh d19.sh

[ `uname` = "Darwin" ] || exit 1
basedir=/System/Library/Frameworks/JavaVM.framework
version=${VERSION-1.6}
echo "[INFO] current java settings:"
for path in `which java` `which javac`
do
    ls -l $path |awk '{print $9,$10,$11}'
done
echo "[INFO] available java versions:"
ls -l $basedir/Versions |awk 'NF > 10 {print $9,$10,$11}'
echo "[INFO] change current version to $version:"
cat <<EOT
cd $basedir/Versions
rm Current && ln -s $version Current
rm CurrentJDK && ln -s $version CurrentJDK
EOT
read -t 10 -p "run them:[y/n]"

if [ $REPLY = "y" ]
then
    cd $basedir/Versions
    rm Current && ln -s $version Current
    rm CurrentJDK && ln -s $version CurrentJDK
fi

