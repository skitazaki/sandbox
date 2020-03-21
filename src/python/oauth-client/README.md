OAuth Client Samples
====================
OAuth 1.0 の認証を行うサンプル実装です。
Twitter べったりにしないで、ベンダーニュートラルなサンプルにします。

サンプルで実装している言語は次の通りです。

- Python
- JavaScript

OAuth 2.0 のサンプル実装はありません。

基本的な準備
------------
サービスプロバイダーにアプリケーションを登録します。
アプリケーションの種類は Web アプリとクライアントアプリがあると思いますが、
配備する方法によって適切な方を選択してください。
ちなみに、クライアントアプリだと確認コードを目にできるため、ネゴシエーションの理解に役立つと考えられます。

種類を選択できないサービスプロバイダーは... やめた方が良いかもしれません。

このサンプルはいくつかの外部ライブラリを必要とします。
事前にシステム標準の方法でインストールするか、パスが通っている場所に配置してください。

設定
----
`settings.ini.sample` をコピーして、`settings.ini` とします。

アプリケーションの Consumer Key と Consumer Secret を `settings.ini` に記述します。
接続するサービスプロバイダーから取得したキーとシークレットを指定してください。

Python
------
Python のバージョンは 2.5 以上を使用してください。

``setuptools`` を使う場合は次のコマンドを実行してください。
Windows 環境の場合はコマンドプロンプトを管理者権限で立ち上げて実行してください。``sudo`` と同じ効果です。
``easy_install`` までのパスはシステムによって異なるかもしれません。

    $ sudo easy_install oauth
    $ sudo easy_install twitter

[virtualenv](http://pypi.python.org/pypi/virtualenv) を使う場合は好きに設定してください。

コマンドラインから実行します。
__-f__ オプションで設定ファイル (`settings.ini`) へのパスを指定できます。
サービスプロバイダーとして _cybozulive_ を使う場合には次のように実行します。

    $ python python/sample.py cybozulive

SQLite のデータを扱う場合には手持ちのツールを使ってください。
使えるものがない場合には Adobe AIR で動く [Lita][Lita] が便利です。

[Lita]: http://www.dehats.com/drupal/?q=node/58

JavaScript
----------
Apache のような Web サーバを用意して、その静的コンテンツ置き場に配置してください。
サーバ側のアプリケーションも実装していく場合には Google App Engine の開発環境が便利だと思います。

Python の _SimpleHTTPServer_ モジュールをコマンドラインから利用すると、8000番ポートでカレントディレクトリのコンテンツを HTTP 経由で公開できます。
コマンドラインから Web サーバを起動させて、Web ブラウザで http://localhost:8000/oauth.html にアクセスしてください。

    $ make prepare
    $ make build
    $ cd js
    $ python -m SimpleHTTPServer

Python 3 系の場合には _SimpleHTTPServer_ ではなく _http.server_ モジュールになります。

なお、Google の CDN から _jQuery_ などのライブラリを読み込みますので、インターネット環境に接続されていることを確認してください。

(!) `make` に依存しているので、Python で書き直す。
    ライブラリのダウンロードと、設定情報の差し込みを実現する。

シグネチャは開発用コンソールで確認してください。

Links
-----
* [OAuthプロトコルの中身をざっくり解説してみるよ][OAuth lecture]
* [OAuth Signature 生成サンプル][OAuth signature sample]

[OAuth signature sample]: http://cgi.geocities.jp/ydevnet/techblog/sample/signature.html
[OAuth lecture]: http://d.hatena.ne.jp/yuroyoro/20100506/1273137673

<!-- vim: set et ts=4 sw=4 cindent fileencoding=utf-8 textwidth=120 : -->
