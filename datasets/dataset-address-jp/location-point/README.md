# Address Datasets in Japan

## 位置参照情報

位置参照情報は 国土交通省 国土政策局 国土情報課 が提供する情報で、http://nlftp.mlit.go.jp/isj/ からダウンロードできるデータです。
「街区レベル位置情報参照情報」と「大字・町丁目レベル位置参照情報」があります。

* 「街区レベル位置参照情報」とは、全国の都市計画区域相当範囲を対象に、街区単位の位置座標を整備した データです。

* 「大字・町丁目レベル位置参照情報」とは、日本における住所体系のうち、
  市、町、村、区、特別区の直下に属す行政区である「大字」、「町丁目」、 自治体によっては「町字」を示す住所代表点と、
  その住所代表点が示す位置座標を対応づけた情報のことです。

### 使い方

CSV ファイルをダウンロードしてデータベースに読み込みます。
スキーマは `datapackage.json` から生成してください。

「街区レベル位置情報参照情報」の例

```sql
CREATE TABLE city_block (
    prefecture      VARCHAR(200) NOT NULL,
    city            VARCHAR(200) NOT NULL,
    town            VARCHAR(200) NOT NULL,
    city_block      VARCHAR(200) NOT NULL,
    csnum           TINYINT UNSIGNED NOT NULL,
    csx             DOUBLE NOT NULL,
    csy             DOUBLE NOT NULL,
    latitude        DOUBLE NOT NULL,
    longitude       DOUBLE NOT NULL,
    house_display   TINYINT UNSIGNED NOT NULL,
    main_city_block TINYINT UNSIGNED NOT NULL,
    update_before   TINYINT UNSIGNED NOT NULL,
    update_after    TINYINT UNSIGNED NOT NULL
) ENGINE InnoDB DEFAULT CHARSET utf8;

LOAD DATA LOCAL INFILE 'city_block.csv' INTO TABLE city_block
CHARACTER SET utf8
FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY ''
IGNORE 1 LINES;
```

「大字・町丁目レベル位置参照情報」の例

```sql
CREATE TABLE town (
    prefecture_code   CHAR(2) NOT NULL,
    prefecture        VARCHAR(200) NOT NULL,
    city_code         CHAR(5) NOT NULL,
    city              VARCHAR(200) NOT NULL,
    town_code         CHAR(12) NOT NULL,
    town              VARCHAR(200) NOT NULL,
    latitude          DOUBLE NOT NULL,
    longitude         DOUBLE NOT NULL,
    original_resource TINYINT UNSIGNED NOT NULL,
    type_code         TINYINT UNSIGNED NOT NULL
) ENGINE InnoDB DEFAULT CHARSET utf8;

LOAD DATA LOCAL INFILE 'town.csv' INTO TABLE town
CHARACTER SET utf8
FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY ''
IGNORE 1 LINES;
```

### 注意事項

利用約款より抜粋：

* 市町村資料、国土地理院の数値地図2500、民間の地図等を基に作成したものであり、国内の標準的な地名を 指定しているものではありません。
* 都市計画区域担当範囲のみ整備されており、全国のデータが揃っているわけではありませんので、利用者は整備範囲等を十分確認の上ご利用ください。
* 位置参照情報は、国土計画関連業務のために作成されたものですので、公共測量等の高度な精度が要求される測量、各種証明等には使用することができません。
* 位置参照情報に含まれる地名は、市町村資料、国土地理院の数値地図2500、民間の地図等を基に作成したものであり、
  国内の標準的な地名を指定しているものではありません。
* データには誤りがある可能性もあります。

出典: 位置参照情報　国土交通省

| レベル | 整備年度 | 版数 |
|-------|---------|------|
| 街区 | 平成23年 | 10.0a |
| 大字・町丁目 | 平成23年 | 5.0b |

更新方法
--------

ダウンロードサイトから ZIP アーカイブを取得して `original` ディレクトリに置きます。

ZIP アーカイブに含まれる CSV ファイルは、異なる住所レベルでも都道府県ごとに同じファイル名になっています。
重複上書きを避けるため、それぞれのレベル名のディレクトリを作成してそこに展開します。

ファイルは都道府県別になっていますので、結合して ``datapackage.json`` のフィールド名を割り当てます。
全国規模の場合、街区は1000万件以上ありますので、全データを結合するにはしばらく時間がかかります。
全国規模の場合、大字は25万件程度なので、まずはこちらから試してみましょう。

```bash
$ mkdir v10.0a v05.0b
$ cd v10.0a
$ for f in ../original/*-10.0a.zip; do unzip $f; done
$ cd ../v05.0b
$ for f in ../original/*-05.0b.zip; do unzip $f; done
$ cd ..
$ ./scripts/concat.py -o town.csv v05.0b/*.csv -vv
$ ./scripts/concat.py -o city_block.csv v10.0a/*.csv -vv
$ gzip town.csv
$ gzip city_block.csv
```
