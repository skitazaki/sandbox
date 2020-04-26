# Japanese Population by Grid Mesh

国土交通省の[国土数値情報ダウンロードサービス](http://nlftp.mlit.go.jp/ksj/)で公開されている「メッシュ別将来人口推計」データを利用できるようにします。
1kmメッシュと500mメッシュのデータがあります。
500mメッシュの変換処理を `convert.ipynb` に記載しています。

都道府県コード、市区町村コードから名称を取得する場合には[住所.jp](http://jusyo.jp/index.html)のデータを参照してください。

## データ変換

データ変換には PostGIS と `shp2pgsql` を使います。

- PostGIS 環境の用意
- ファイルをダウンロード
- Zip 形式のデータを展開
- Shape 形式のデータを PostGIS にインポート
- いくつかの形式でデータを出力
    - 都道府県ごとの GeoJSON ファイル
    - 一次メッシュごとの GeoJSON ファイル
    - 形状情報を含まない CSV ファイル

Reference:

* [PostGISからGeoJSON出力するときに属性を付与する - Qiita](http://qiita.com/kshigeru/items/8940ecf7f261a6b01ed0)

## メタデータ

メタデータは [Data Package](https://frictionlessdata.io/specs/data-package/) 形式で管理します。
データ自体はGitリポジトリでは管理しません。

`datapackage.yaml` を手動で編集し、Python を使って `datapackage.json` に変換します。

```bash
$ pipenv run python scripts/yaml2json.py population-mesh/datapackage.yaml
```

[goodtables](https://github.com/frictionlessdata/goodtables-py) でデータクオリティを確認します。

```bash
$ pipenv run goodtables datapackage.json
```
