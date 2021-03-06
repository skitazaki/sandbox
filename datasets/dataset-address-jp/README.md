# Address Datasets in Japan

日本の住所に関するデータをいくつかピックアップして整形します。

## 基本情報

都道府県コードと市区町村コードを **base** パッケージとしてまとめます。
日本郵便株式会社の郵便番号データをベースにしていますので、市区町村コードに変更があるかもしれません。

その他の情報は[住所.jp](http://jusyo.jp/index.html)のデータを参照してください。

## 地理情報

GeoJSON 形式のデータ項目を PostGIS に読み込むには `ST_GeomFromGeoJSON()` 関数を使って変換してください。
Postgres の **COPY** を使って読み込むことはできません。

### 統計メッシュ

### 住所境界

### 位置参照情報

## 統計情報

### メッシュ別将来人口推計

## メタデータ

メタデータは [Data Package](https://frictionlessdata.io/specs/data-package/) 形式で管理します。
データ自体はGitリポジトリでは管理しません。

`datapackage.yaml` を手動で編集し、Python を使って `datapackage.json` に変換します。

```bash
$ pipenv run python yaml2json.py base/datapackage.yaml
$ pipenv run python yaml2json.py geo-grid/datapackage.yaml
$ pipenv run python yaml2json.py population-mesh/datapackage.yaml
$ pipenv run python yaml2json.py location-point/datapackage.yaml
```

[goodtables](https://github.com/frictionlessdata/goodtables-py) でデータクオリティを確認します。

```bash
$ pipenv run goodtables base/datapackage.json
```
