#!/bin/sh
# prepare a project for Widgets
# example: sh d59.sh sampleproj
# (http://www.w3.org/TR/widgets/)

DEVELOPER_NAME="Shigeru Kitazaki"
DEVELOPER_URL="http://skitazaki.appspot.com"

project=$1
mainfile=$project.js

die() { echo $1; exit 1; }
[ -z $project ] && die "specify project name."
[ -d $project ] && die "project \"$project\" already exists."

# check "ant" is available.
ant=ant
$ant -version >/dev/null;   [ $? -eq 0 ] || exit 1

currentdir=`pwd`
mkdir $project; cd $project

cat <<EOF >build.xml
<?xml version="1.0"?>
<project name="$project - Widget" default="default" basedir=".">

    <property name="build.dir" location="build"/>
    <property name="src.dir" location="src"/>

    <target name="all" depends="clean, default">
    </target>

    <target name="init">
        <tstamp>
            <format property="TODAY" pattern="yyyy/MM/dd"/>
        </tstamp>
        <mkdir dir="\${build.dir}"/>
    </target>

    <!--
      ~ http://ant.apache.org/manual/Tasks/zip.html
     -->
    <target name="default" depends="init, copy">
        <zip destfile="$project.wgt"
             basedir="\${build.dir}" />
    </target>

    <target name="copy">
        <copy file="\${src.dir}/config.xml" todir="\${build.dir}"/>
        <copy file="\${src.dir}/index.html" todir="\${build.dir}"/>
        <copy file="\${src.dir}/style.css"  todir="\${build.dir}"/>
        <copy file="\${src.dir}/$mainfile"  todir="\${build.dir}"/>
    </target>

    <target name="clean">
        <delete dir="\${build.dir}"/>
        <delete file="$project.wgt"/>
    </target>
</project>
EOF

mkdir src
cat <<EOF >src/index.html
<!DOCTYPE html>
<html><head>
<meta charset="utf-8"/>
<meta name="viewport"
      content="width=device-width,user-scalable=no,initial-scale=1.0"/>
<title>$project</title>
<link rel="stylesheet" type="text/css" href="style.css" />
</head><body>
<h1>Hello $project</h1>
<script type="text/javascript" src="$mainfile"></script>
</body></html>
EOF

cat <<EOF >src/config.xml
<?xml version="1.0" encoding="UTF-8"?>
<widget xmlns="http://www.w3.org/ns/widgets"
        id="http://example.org/exampleWidget" version="0.1"
        height="320"  width="320"
        viewmodes="application">
    <name>Hello $project</name>
    <description>My First Application</description>
    <author href="$DEVELOPER_URL">$DEVELOPER_NAME</author>
</widget>
EOF
cat <<EOF >src/style.css
EOF

cat <<EOF >src/$mainfile
(function(d) {
    var space = d.createElement("div");
    setInterval(function(){
        space.innerHTML = "" + new Date();
    }, 1000);
    d.body.appendChild(space);
}(document));
EOF

$ant

cd $currentdir

