<?php
/**
 * Sample usage of sqlite
 * example: php -f d54.php
 * see also "d35.py", Python version of SQLite.
 */

const TABLE_NAME = "stocks";
const DATA_AMOUNT = 50;

$TRANS_TYPE = array("BUY", "SELL");
$SYMBOL_TYPE = array("Apple", "Google", "Microsoft", "Sony");

$fname = ":memory";
$dns = "sqlite:".$fname;
$db = new PDO($dns);
//CREATE////////////////////////////////////////////////////////////////////
$ret = $db->query("SELECT sql FROM sqlite_master
        WHERE type='table' AND tbl_name='".TABLE_NAME."'");
if ($r = $ret->fetch()) {
    echo "'".TABLE_NAME."' is already created: ".$r[0].PHP_EOL;
} else {
    $db->query("CREATE TABLE ".TABLE_NAME." (
        date TEXT, trans TEXT, symbol TEXT, qty REAL, price REAL)");
    echo "create a table: '".TABLE_NAME."'".PHP_EOL;
}

//INSERT////////////////////////////////////////////////////////////////////
$stmt = $db->prepare("INSERT INTO ".TABLE_NAME.
        " (date,trans,symbol,qty,price) VALUES (?,?,?,?,?)");
if (!$stmt)
    die("Invalid statement.");

for ($i = 0; $i < DATA_AMOUNT; $i++) {
    $d = sprintf("20%02d-%02d-%02d",
            mt_rand(0,10), mt_rand(1,12), mt_rand(1,31));
    $stmt->execute(array($d, $TRANS_TYPE[mt_rand(0,1)],
        $SYMBOL_TYPE[mt_rand(0,3)], mt_rand(1, $i+1), mt_rand(100, 1000000)));
}

//SELECT////////////////////////////////////////////////////////////////////
$ret = $db->query("SELECT * FROM ".TABLE_NAME);
foreach ($ret as $r) {
    printf("%s %-5s %-10s %5d %8d\n", $r[0], $r[1], $r[2], $r[3], $r[4]);
}

