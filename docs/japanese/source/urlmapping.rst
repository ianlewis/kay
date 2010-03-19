==============
URL マッピング
==============

概要
----

Kay は URL と view を関係付けるのに Werkzeug を使っています。

URL マッピングをどのように編集するかについて更に詳しく知るには、下記の URL にホストされている werkzeug のマニュアルを見ると良いでしょう:

  http://werkzeug.pocoo.org/documentation/0.6/routing.html

現バージョンの Kay では ``SUBMOUNT_APP`` 機能を使わない限りは、プロジェクトにつき、ひとつのグローバルな url マッピングとひとつの endpoint-view の対応辞書を持ちます。Kay はこれらの値を、インストールされたアプリケーション( ``settings.py`` での設定によります)から自動的に収集し、グローバルな値として保持します。

どのように動作するか
--------------------

``manage.py startapp`` コマンドにより作成されたアプリケーションには、デフォルトの ``urls.py`` が含まれています。この中には ``RuleFactory`` または ``Rule`` を返す ``make_rules`` 関数が用意されています。

Kay は ``appname.urls`` モジュールを検知すると、この ``RuleFactory`` をグローバルな url マッピングに組み込みます。

このルールはデフォルトでは ``/appname`` にマウントされます。このマウントポイントは ``APP_MOUNT_POINTS`` へ ``{'appname': '/mount_path'}`` 形式で指定する事で変更できます。

デフォルトの ``urls.py`` はモジュールグローバルな ``all_views`` という辞書があります。Kay はこの辞書も検知して自動的にグローバルな設定に組み込みます。

ビューを追加する
----------------

独自のビューを追加するには、アプリケーションディレクトリ内の ``urls.py`` を編集する必要があります。
``myapp`` というアプリケーションがあるとして、そこに独自のビューを追加したいとしましょう。デフォルトの ``urls.py`` には ``/myapp/`` という url に結びついた ``index`` ビューがあります。デフォルトの ``urls.py`` は下記のようになっています:

.. code-block:: python

  from werkzeug.routing import EndpointPrefix, Rule

  import myapp.views

  def make_rules():
    return [
      EndpointPrefix('myapp/', [
	Rule('/', endpoint='index'),
      ]),
    ]

  all_views = {
    'myapp/index': myapp.views.index,
  }

下記の例では ``index2`` ビューを ``/myapp/index2`` という url に結び付けています:

.. code-block:: python

  from werkzeug.routing import EndpointPrefix, Rule

  import myapp.views

  def make_rules():
    return [
      EndpointPrefix('myapp/', [
	Rule('/', endpoint='index'),
	Rule('/index2', endpoint='index2'),
      ]),
    ]

  all_views = {
    'myapp/index': myapp.views.index,
    'myapp/index2': myapp.views.index2,
  }

上記の例では、関数オブジェクト自体を view として定義しています。そのためには、 ``views`` モジュールをインポートしておく必要があります。しかし ``views`` モジュールがとても大きかったり、またプロジェクト内にたくさんのアプリケーションが存在する場合などには、このやり方はスタートアップ時の大きなコストにつながる可能性がありますので、このコストを避けるために view を文字列で定義する事もできます。そうする事により、view を必要になった時にはじめて読み込む(遅延ロードする)事ができるようになります。

最後の例を文字列で view を定義するように書き直したバージョンを下記に示します。ここで注意するのは ``import myapp.views`` の行を削除しないと、遅延ロードの効果が無いという事です。

.. code-block:: python

  from werkzeug.routing import EndpointPrefix, Rule

  def make_rules():
    return [
      EndpointPrefix('myapp/', [
	Rule('/', endpoint='index'),
	Rule('/index2', endpoint='index2'),
      ]),
    ]

  all_views = {
    'myapp/index': 'myapp.views.index',
    'myapp/index2': 'myapp.views.index2',
  }

時にはクラスベースのビューを作成する事もあります。そのようなビューを遅延ロードさせるためには下記のように設定します:

.. code-block:: python

  from werkzeug.routing import EndpointPrefix, Rule

  def make_rules():
    return [
      EndpointPrefix('myapp/', [
	Rule('/', endpoint='index'),
	Rule('/index2', endpoint='index2'),
      ]),
    ]

  all_views = {
    'myapp/index': 'myapp.views.index',
    'myapp/index2': ('myapp.views.MyClassBasedView', (),
                     {"template_name": "myapp/mytemplate.html"}),
  }

この例では、 ``MyClassBasedView`` のインスタンスが要求に応じて下記と同
等の方法で生成されます:

.. code-block:: python

   from myapp.views import MyClassBasedView
   view_func = MyClassBasedView(template_name="myapp/mytemplate.html")

.. seealso:: :doc:`views`

