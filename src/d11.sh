#!/bin/sh
# Retrieve RFC documents, and split them into page by page.

if [ $# -lt 1 ]; then
    cat <<EOT
Usage:
    $0 rfc_number [rfc_number..]
EOT
    exit 1
fi

endpoint=http://www.ietf.org/rfc

for n in $*; do
    rfc=rfc$n.txt
    if [ ! -f $rfc ]; then
        wget -O $rfc $endpoint/$rfc
    fi
    cat $rfc |
    awk '{
        if($0 == "\f" || !output)
            output = sprintf("rfc'$n'-%03d.txt", ++page);
        else
            print $0 >> output;
    }'
done

