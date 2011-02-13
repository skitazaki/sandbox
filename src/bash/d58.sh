#!/bin/sh
# sample usage of sqlite3
# example: sh d58.sh

DATABASE=d58.sqlite
SQLITE="sqlite3 $DATABASE"
TABLE_NAME="stocks"

ret=`$SQLITE "SELECT sql FROM sqlite_master WHERE type='table' \
         AND tbl_name='$TABLE_NAME';"`
if [ -n "$ret" ]
then
    echo "$TABLE_NAME is already created: $ret"
else
    $SQLITE "CREATE TABLE $TABLE_NAME ( \
         date TEXT, trans TEXT, symbol TEXT, qty REAL, price REAL);"
    echo "create a table: '$TABLE_NAME'"
fi

for i in {1..50}
do
    let y=$RANDOM%11
    let m=$RANDOM%12+1
    let d=$RANDOM%31+1
    date=`printf "20%02d-%02d-%02d" $y $m $d`
    trans="BUY"
    symbol="Apple"
    qty=$RANDOM
    price=$RANDOM
    $SQLITE "INSERT INTO $TABLE_NAME (date,trans,symbol,qty,price) VALUES \
        ('$date','$trans','$symbol','$qty','$price');"
done

$SQLITE "SELECT * FROM $TABLE_NAME;" |
    awk 'BEGIN { FS="|" }
        { printf "%s %-5s %-10s %5d %8d\n", $1, $2, $3, $4, $5 }'

