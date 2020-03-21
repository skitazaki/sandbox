#!/bin/sh
#/ Usage: ./build.sh

set -eu

BASEDIR=$(cd $(dirname $0) && pwd)
# Version number to tag the docker container. (not implemented yet.)
# VERSION=

CLIENT_DIR=$BASEDIR/client

# Build client assets.
cd $CLIENT_DIR
docker build --rm --no-cache -t my/nodejs-build .
[ -d dist ] && rm -fr dist
mkdir dist
docker run -v `pwd`/dist:/tmp/dist --rm -it my/nodejs-build "cp -pr /app/dist /tmp"

cd $BASEDIR

# Build server side container and test it.
docker build --rm --no-cache -t my/dashboard .
# Be sure to run docker container named with "postgres" before testing.
docker run -p 8080:80 --rm -it --link postgres:postgres my/dashboard "env"
