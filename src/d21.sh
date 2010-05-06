#!/bin/sh
# Shorten URL with "goo.gl".
# http://www.commandlinefu.com/commands/view/5182/google-url-shortener
# example:
# $ sh d21.sh "http://www.google.com/search?q=hello" "http://google.com"

if [ $# -eq 0 ]; then
    echo "usage: $0 url [url ...]"
    exit 1
fi
for u in "$@"; do
    curl -s 'http://ggl-shortener.appspot.com/?url='"$u" |
        sed -e 's/{"short_url":"//' -e 's/"}/\n/g'
done

