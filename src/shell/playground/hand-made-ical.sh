#!/bin/sh
# Hand-made iCal file.
#
# CAUTION: The end of line must be CRLF.
# NOTE: This does not manage timezone feature.
# See http://tools.ietf.org/html/rfc2445

if [ $# -lt 1 ]; then
    echo "Give me CSV file(s)."
    echo "Format: YYYYMMDD,Summary,Description"
    exit 1
fi
file=$@

uid=$USERNAME

cat <<EOT
BEGIN:VCALENDAR
PRODID:-//KITAZAKI Shigeru//Hand-made//EN
VERSION:2.0
EOT
cat $file |
awk 'BEGIN { FS="," } {
    print "BEGIN:VEVENT"
    print "UID:'`date "+%Y%m%d%H%M%S"`'-"NR"-'$uid'"
    print "SUMMARY:"$2
    print "DTSTART:"$1
    print "DESCRIPTION:"$3
    print "CLASS:PRIVATE"
    print "DTSTAMP:'`date --utc "+%Y%m%dT%H%M%SZ"`'"
    print "END:VEVENT"
}'
cat <<EOT
END:VCALENDAR
EOT
