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


view に引数を渡す
-----------------

``<variable_name>`` というようにマークする事で、URL に変数を設定できま
す。これらの値は view にキーワード引数として渡されます。例をいくつか:

.. code-block:: python

  from werkzeug.routing import EndpointPrefix, Rule

  def make_rules():
    return [
      EndpointPrefix('myapp/', [
	Rule('/', endpoint='index'),
	Rule('/user/<username>', endpoint='user'),
	Rule('/post/<int:post_id>', endpoint='post')
      ]),
    ]

  all_views = {
    'myapp/index': 'myapp.views.index',
    'myapp/user': 'myapp.views.show_user_profile',
    'myapp/post': 'myapp.views.show_post',
  }


これらの値を受け取れるように view を書いてください。

.. code-block:: python

  # -*- coding: utf-8 -*-

  from werkzeug import Response
  from kay.utils import render_to_response

  # ..

  def show_user_profile(request, username):
    # ..
    # ..

  def show_post(request, post_id)
    # ..
    # ..

Introducing a new interface for urlmapping
------------------------------------------

.. Note::

  This interface is still under experimental stage, so detailed
  implementation/usage might change in the future.

In the new urlmapping system, you need to define ``view_groups``
global variable in your urls.py. The value must be a list or tuple of
ViewGroup instances.

``ViewGroup`` is a class which holds url rules and endpoint-view
mappings as its instance attributes. You can pass unlimited number of
``Rule`` instances to a constructor method of this class.

A constructor of ``Rule`` class accepts not only all the arguments
suitable for ``werkzeug.routing.Rule`` class's constructor but also
accepts ``view`` keyword argument.

Let's see the simplest example.

urls.py:

.. code-block:: python

  from kay.routing import (
    ViewGroup, Rule
  )

  view_groups = [
    ViewGroup(Rule('/', endpoint='index', view='myapp.views.index'))
  ]

By default, endpoint is prefixed with ``app_name/`` automatically, so
in this example, you need to pass 'myapp/index' to ``url_for()``
helper function.

To suppress this prefixing, you can just pass
``add_app_prefix_to_endpoint`` keyword argument with ``False`` value.
You can also define your own ViewGroup subclass and override
``add_app_prefix_to_endpoint`` class attribute to False:

Suppressing the prefix:

.. code-block:: python

  from kay.routing import (
    ViewGroup, Rule
  )

  view_groups = [
    ViewGroup(Rule('/', endpoint='index', view='myapp.views.index'),
              add_app_prefix_to_endpoint=False)
  ]


Please be aware an endpoint which is defined once will never be
overridden by following definition, because endpoint-view mapping is
just a dictionary.

If you need to define two or more Rules with the same endpoint, you
can omit redundant view keyword arguments in this case as follows:

.. code-block:: python

  view_groups = [
    ViewGroup(
      Rule('/list_entities', endpoint='index', view='myapp.views.index'),
      Rule('/list_entities/<cursor>', endpoint='index')
    )
  ]
