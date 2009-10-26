=============
ミドルウェア
=============

ミドルウェア (Middleware) とは、 Kay のリクエスト/レスポンス処理をフックするためのフレームワークです。ミドルウェアは軽量かつ低水準な「プラグイン」システムで、Kay の入出力を操作します。

各ミドルウェアコンポーネントはそれぞれ特定の機能を担っています。例えば、Kay には ``AuthenticationMiddleware`` ミドルウェアコンポーネントがありますが、これはアプリケーションに認証機能を追加します。

このドキュメントでは、 Kay についてくる全てのミドルウェアコンポーネントの使用法と、自分で新たにミドルウェアを作る方法を説明します。

Kay には、すぐに使える組み込みのミドルウェアが付属しています。 :doc:`builtin-middleware` を参照してください。

.. _Activating middleware:

ミドルウェアの有効化
====================

ミドルウェアコンポーネントを有効化するには、Kay 設定ファイルの :attr:`settings.MIDDLEWARE_CLASSES` リストにコンポーネントを追加します。コンポーネント名は文字列で指定し、ミドルウェアのクラス名を完全な Python パスで表します。例えば、 ``manage.py startproject`` が生成するデフォルトの設定ファイルにある ``MIDDLEWARE_CLASSES`` は以下のようになっています::

    MIDDLEWARE_CLASSES = (
        'kay.auth.middleware.AuthenticationMiddleware',
    )

リクエストの処理フェーズでは、Kay は :attr:`settings.MIDDLEWARE_CLASSES` に指定された順番で (:meth:`process_request` および :meth:`process_view`) ミドルウェアを適用していきます。レスポンスの処理フェーズでは、(:meth:`process_response` および :meth:`process_exception` ) ミドルウェアが逆順に適用されます。この仕組みは、タマネギの構造になぞらえて、ミドルウェアクラスを「層」だと考えるとよいでしょう:

Kay はミドルウェアがなくても動作します -- 望むなら :attr:`settings.MIDDLEWARE_CLASSES` は空でもよいのです。

.. _Writing your own middleware:

ミドルウェアを自作する
======================

ミドルウェアの自作は簡単です。各ミドルウェアコンポーネントは、以下のメソッドを少なくとも一つ定義しているような単一の Python クラスです:

.. _request-middleware:

``process_request``
-------------------

.. method:: process_request(self, request)

``request`` は :class:`werkzeug.Request` オブジェクトです。このメソッドはリクエストごとに Kay がどのビューを実行するか決定する前に呼び出されます。

``process_request()`` は ``None`` または :class:`werkzeug.Response` オブジェクトのいずれかを返さねばなりません。 ``None`` を返した場合、 Kay はリクエストの処理を継続し、他のミドルウェアや適切なビューを実行します。 :class:`werkzeug.Response` オブジェクトを返した場合、 Kay は他のリクエストミドルウェア、ビューミドルウェア、例外ミドルウェア、あるいは URLconf で設定されたビューを呼び出さず、 :class:`werkzeug.Response` オブジェクトをそのまま返します。レスポンスミドルウェアは必ず呼び出されます。

.. _view-middleware:

``process_view``
----------------

.. method:: process_view(self, request, view_func, view_args, view_kwargs)

``request`` は :class:`werkzeug.Request` オブジェクトです。 ``view_func`` は Kay がビュー関数としてこれから呼び出そうとしている Python の関数です (実際の関数オブジェクトで、関数名を表す文字列ではありません)。 ``view_args`` にはビューに渡されることになる固定引数が、 ``view_kwargs`` にはビューに渡されることになるキーワード引数のディクショナリが入っています。 ``view_args`` と ``view_kwargs`` のいずれにも、ビューの第一引数 (``request``) は入っていません。

``process_view()`` は Kay がビュー関数を呼び出す直前に呼び出されます。この関数は ``None`` または :class:`werkzeug.Response` オブジェクトを返さねばなりません。 ``None`` を返した場合、 Kay は処理を継続し、他のミドルウェアの ``process_view()`` を試した後、適切なビュー関数を呼び出します。 :class:`werkzeug.Response` オブジェクトを返した場合、 Kay は他のリクエストミドルウェア、ビューミドルウェア、例外ミドルウェア、あるいは URLconf で設定されたビューを呼び出さず、 :class:`werkzeug.Response` オブジェクトをそのまま返します。レスポンスミドルウェアは必ず呼び出されます。

.. _response-middleware:

``process_response``
--------------------

.. method:: process_response(self, request, response)

``request`` は :class:`werkzeug.Request` オブジェクトです。 ``response`` は Kay のビュー関数の返す :class:`werkzeug.Response` オブジェクトです。

``process_response()`` は :class:`werkzeug.Response` オブジェクトを返さねばなりません。渡された ``response`` オブジェクトを変更して返しても、新たに :class:`werkzeug.Response` オブジェクトを生成して返してもかまいません。

.. _exception-middleware:

``process_exception``
---------------------

.. method:: process_exception(self, request, exception)

``request`` は :class:`werkzeug.Request` オブジェクトです。 ``exception`` はビュー関数の送出した ``Exception`` オブジェクトです。

Kay はビューが例外を送出した際に ``process_exception()`` を呼び出します。 ``process_exception()`` は ``None`` または :class:`werkzeug.Response` オブジェクトのいずれかを返さねばなりません。 :class:`werkzeug.Response` オブジェクトを返した場合、その応答をそのままブラウザに返します。それ以外の場合、デフォルトの例外処理を起動します。

``__init__``
------------

ほとんどのミドルウェアクラスは、実質的に単なる ``process_*`` メソッドの置き場でしかないので、初期化メソッドは必要ありません。ミドルウェアのグローバルな状態を保存するのに ``__init__`` メソッドを使ってもかまいませんが、以下の点に注意してください:

    * Kay はミドルウェアクラスを引数なしで初期化するので、 ``__init__`` には必須の引数を定義できません。

    * ``process_*`` メソッドはリクエストごとに呼び出されますが、 ``__init__`` は Web サーバの起動時に *一度* しか呼び出されません。

.. Marking middleware as unused

ミドルウェアを動的に有効にする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ミドルウェアを使うかどうかを実行時に決められると便利なことがあります。ミドルウェアの ``__init__`` メソッドで
:exc:`kay.exceptions.MiddlewareNotUsed` を送出すると、 Kay はそのミドルウェアを処理から外します。

.. _Guidelines:

ガイドライン
------------

    * ミドルウェアのクラスはサブクラスでなくてもかまいません。

    * ミドルウェアのクラスはPython のモジュールパス上のどこにでも置けます。 Kay にとって必要なのは :attr:`settings.MIDDLEWARE_CLASSES` にクラスへのパスが指定されていることだけです。

    * :doc:`builtin-middleware` を参考にしてください。

    * 自分の書いたミドルウェアコンポーネントが他の人にとっても有用だと思ったなら、ぜひ `コミュニティにコントリビュート <http://groups.google.com/group/kay-users-ja>`_ してください！ 知らせてくだされば、 Kay に追加するか検討します。
