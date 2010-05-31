#!/bin/sh
# switches JDK version on MacOSX.
# example
# $ sh d19.sh 1.6

[ `uname` = "Darwin" ] || exit 1
basedir=/System/Library/Frameworks/JavaVM.framework
version=${1-1.6}
echo "[INFO] current java settings:"
for path in `which java` `which javac`
do
    ls -l $path |awk '{print $9,$10,$11}'
done
echo "[INFO] available java versions:"
ls -l $basedir/Versions |awk 'NF > 10 {print $9,$10,$11}'
echo "[INFO] change current version to $version:"
cat <<EOT
------------------------------------------------------------
    cd $basedir/Versions
    rm CurrentJDK && ln -s $version CurrentJDK
EOT
read -t 10 -p "run them? [y/N]:"

[ -z $REPLY ] && exit 1

if [ $REPLY = "y" ]
then
    cd $basedir/Versions
    rm CurrentJDK && ln -s $version CurrentJDK
fi

