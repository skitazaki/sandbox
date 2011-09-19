#!/bin/sh
# Pull in upstream changes for `JavaScriptMVC`
# See http://help.github.com/fork-a-repo/

modules=(jquery steal documentjs funcunit)

for module in ${modules[@]}
do
    echo "--- Update -->" $module
    pushd $module
    git fetch upstream
    git merge upstream/master
    git st
    popd
done
