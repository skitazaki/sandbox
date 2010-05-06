#!/bin/sh
# [http://gauc.no-ip.org/awk-users-jp/blis.cgi/DoukakuAWK_263]
# example:
# $ location=Tokyo sh d03.sh
#
# Output is UTF-8 by 'nkf' command.
#
# Prerequisite:
# * wget, sed, awk (standard tools)
# * xml2
# * nkf

endpoint="http://www.google.com/ig/api"
location=${location-"Tokyo"}

# get xml response and pritify it
wget -q -O - "$endpoint?weather=$location&hl=ja" |
xml2 | sed 's:/xml_api_reply/weather/::' |
awk 'BEGIN { FS="/" }
$1 == "current_conditions" && $2 == "temp_c" {
    print "Today'\''s Temperature: " substr($3, 7) "C"
}
$1 == "forecast_conditions" {
    if ($2 == "day_of_week")
        print "Day: " substr($3, 7)
    else if ($2 == "low")
        print "\tLow: " substr($3, 7)
    else if ($2 == "high")
        print "\tHigh: " substr($3, 7)
    else if ($2 == "condition")
        print "\tCondition: " substr($3, 7)
}' | nkf -w

