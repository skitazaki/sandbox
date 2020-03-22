#!/bin/sh
# Create a project for HTML5 Widget.
#
# <http://www.w3.org/TR/widgets/>
# <http://satoshi.blogs.com/life/2010/05/widget_entry.html>

DEVELOPER_NAME="YOUR NAME"
DEVELOPER_URL="http://example.com"

project=$1

die() { echo $1; exit 1; }
[ -z $project ] && die "specify project name."
[ -d $project ] && die "project \"$project\" already exists."

mkdir -p $project/src
mkdir -p $project/lib
mkdir -p $project/test
mkdir -p $project/images

ant_build_xml=$project/build.xml
base_html=$project/src/index.html
config_xml=$project/src/config.xml
style_css=$project/src/$project.css
script_js=$project/src/$project.js

cat <<EOF >$ant_build_xml
<?xml version="1.0"?>
<project name="$project - Widget" default="default" basedir=".">

    <property name="build.dir" location="_build"/>
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
        <copy file="\${src.dir}/config.xml"   todir="\${build.dir}"/>
        <copy file="\${src.dir}/index.html"   todir="\${build.dir}"/>
        <copy file="\${src.dir}/$project.css" todir="\${build.dir}"/>
        <copy file="\${src.dir}/$project.js"  todir="\${build.dir}"/>
    </target>

    <target name="clean">
        <delete dir="\${build.dir}"/>
        <delete file="$project.wgt"/>
    </target>
</project>
EOF

cat <<EOF >$base_html
<!DOCTYPE html>
<html><head>
<meta charset="utf-8"/>
<meta name="viewport"
      content="width=device-width,user-scalable=no,initial-scale=1.0"/>
<title>$project</title>
<link rel="stylesheet" type="text/css" href="$project.css" />
</head><body>
<h1>Hello $project</h1>
<script type="text/javascript" src="$project.js"></script>
</body></html>
EOF

cat <<EOF >$config_xml
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

cat <<EOF >$style_css
EOF

cat <<EOF >$script_js
(function(d) {
    var space = d.createElement("div");
    setInterval(function(){
        space.innerHTML = "" + new Date();
    }, 1000);
    d.body.appendChild(space);
}(document));
EOF

echo "Created \"$project\", build it using Ant."
