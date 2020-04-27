# Address Datasets in Japan

日本の住所に関するデータをいくつかピックアップして整形します。
都道府県コード、市区町村コードから名称を取得する場合には[住所.jp](http://jusyo.jp/index.html)のデータを参照してください。

## 位置参照情報

## メッシュ別将来人口推計

## メタデータ

メタデータは [Data Package](https://frictionlessdata.io/specs/data-package/) 形式で管理します。
データ自体はGitリポジトリでは管理しません。

`datapackage.yaml` を手動で編集し、Python を使って `datapackage.json` に変換します。

```bash
$ pipenv run python scripts/yaml2json.py population-mesh/datapackage.yaml
$ pipenv run python scripts/yaml2json.py location-point/datapackage.yaml
```

[goodtables](https://github.com/frictionlessdata/goodtables-py) でデータクオリティを確認します。

```bash
$ pipenv run goodtables datapackage.json
```
