# Japanese Population by Grid Mesh

国土交通省の[国土数値情報ダウンロードサービス](http://nlftp.mlit.go.jp/ksj/)で公開されている「メッシュ別将来人口推計」データを利用できるようにします。
1kmメッシュと500mメッシュのデータがあります。
500mメッシュの GeoJSON への変換処理を [`convert-m500.ipynb`](convert-m500.ipynb) に記載しています。

## データ変換

データ変換には PostGIS と `shp2pgsql` を使います。
変換作業の流れは次のようになります。

- PostGIS 環境の用意  --> Docker Compose で用意
- ファイルをダウンロード  --> 手作業でダウンロード
- Zip 形式のデータを展開
- Shape 形式のデータを PostGIS にインポート
- いくつかの形式でデータを出力
    - 都道府県ごとの GeoJSON ファイル
    - 一次メッシュごとの GeoJSON ファイル
    - 形状情報を含まない CSV ファイル

Docker コンテナに接続し、Zip 形式のデータを展開してから、Shape 形式のデータを PostGIS にインポートする例：

```bash
(host) $ docker-compose exec -u postgres postgis /bin/bash
(container) $ cd /tmp
(container) $ unzip /data/path/to/m500-17_GML.zip
(container) $ shp2pgsql -W Shift_JIS Mesh4_POP_00.shp 2>/dev/null | psql -d postgres
```

ZIP ファイルには Shape ファイルが含まれますので、拡張子が ".shp" のものと、その他に ".dbf" などいくつかのファイルがあります。
ZIP ファイルを展開したファイルを合計すると760MB程度になります。
データベースでのテーブル名は **mesh4_pop_00** になります。
テーブル名を指定するには `shp2pgsql` の第二引数に名称を与えます。

Reference:

* [PostGISからGeoJSON出力するときに属性を付与する - Qiita](http://qiita.com/kshigeru/items/8940ecf7f261a6b01ed0)
