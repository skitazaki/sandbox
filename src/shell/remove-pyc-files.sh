#!/bin/sh
# Clean all .pyc files from current project. It cleans all the files
# recursively.
#
# <http://www.commandlinefu.com/commands/view/7658/clean-all-.pyc-files-from-current-project.-it-cleans-all-the-files-recursively.>`

dir=${1-.}

find $dir -type f -name "*.pyc" -delete;
