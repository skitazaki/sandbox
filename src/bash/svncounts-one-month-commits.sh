#!/bin/sh
#
# shows commit counts per committer.
# see `Top SVN committers
# <http://www.commandlinefu.com/commands/view/7545/top-svn-committers-without-awk>`.
#

if [ -z "$since" ]
then
    days=30
    since=`cat <<EOT |python
import datetime as d; print(d.date.today() - d.timedelta(days=$days))
EOT`
fi
echo "since: $since"
for d in ${*-.}
do
    [ -d $d/.svn ] || continue
    echo "directory: $d"
    svn log -r {$since}:HEAD --stop-on-copy -q $d |
        grep '^r[0-9]' | cut -d"|" -f2 | sort | uniq -c | sort -nr
done

