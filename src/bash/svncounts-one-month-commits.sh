#!/bin/sh
# shows commit counts per committer.

days=30
since=`cat <<EOT |python
import datetime as d; print(d.date.today() - d.timedelta(days=$days))
EOT`

echo "since: $since"
for d in ${*-.}
do
    [ -d $d/.svn ] || continue
    echo "directory: $d"
    svn log -r {$since}:HEAD $d |
    grep '^r[0-9]' | cut -d"|" -f2 | sort | uniq -c
done

