==================
ユーティリティ関数
==================

.. module:: kay.utils

:mod:`kay.utils` には、便利な関数がいろいろ揃っています。

.. function:: set_trace()

   pdb の set_trace を 適切な設定でセットします。

.. function:: raise_on_dev()

   開発環境でのみ、ランタイムエラーをあげます。

.. function:: get_timezone(tzname)

   タイムゾーンを取得します。
   
   :param tzname: タイムゾーンの名称
   :return: datetime.tzinfo の実装

.. function:: url_for(endpoint, **args)

   エンドポイントへの URL を取得します。特殊なキーワード引数をとります。

     `_anchor`: この文字列は URL アンカーとして使われます。

     `_external`: `True` の場合、 フルサーバー名と `http://` プリフィクスつきで、 URL を生成します。

   :param args: キーワード引数は URL を生成するのに使われます。
   :return: エンドポイントへの URL を表す文字列

.. function:: create_login_url(url=None)

   ログインページの URL を取得します。

   :param url: ユーザがログインした後にリダイレクトされる URL です。未指定の場合、現在の URL が使われます。
   :return: ログイン URL を表す文字列

.. function:: create_logout_url(url=None)

   ログアウトページの URL を取得します。

   :param url: ユーザがログアウトした後にリダイレクトされる URL です。未指定の場合、現在の URL が使われます。
   :return: ログアウト URL を表す文字列

.. function:: render_error(e)

   Jinja2 テンプレートを使って、 :class:`werkzeug.exceptions.HTTPException` のインスタンスをレンダリングします。

   :param e: :class:`werkzeug.exceptions.HTTPException` の任意のサブクラスのインスタンスです。
   :return: :class:`werkzeug.Response` のインスタンス

.. function:: render_to_string(template, context={}, processors=None)

   テンプレートレンダリング用の関数です。 :mod:`settings.CONTEXT_PROCESSORS` の設定に従って、
   コンテキスト用の変数を自動的に追加します。
   
   :param template: テンプレートのパス
   :param context: テンプレートに渡すコンテキストのディクショナリ
   :param processors: 必要に応じたプロセッサ
   :return: レンダリングされた文字列

.. function:: render_to_response(template, context, mimetype='text/html', processors=None)

   HTML ページをレンダリングするための関数です。

   :param template: テンプレートのパス
   :param context: テンプレートに渡すコンテキストのディクショナリ
   :param processors: 必要に応じたプロセッサ
   :param mimetype: :class:`werkzeug.Response` の mimetype
   :return: レンダリングされた文字列


.. function:: to_local_timezone(datetime, tzname=settings.DEFAULT_TIMEZONE)

   datetime オブジェクトをローカルタイムゾーンに変換します。
   
   :param datetime: UTC タイムゾーンの datetime オブジェクト
   :param tzname: タイムゾーンの名称
   :return: 新しいタイムゾーンの datetime.datetime object

.. function:: to_utc(datetime, tzname=settings.DEFAULT_TIMEZONE)

   datatime オブジェクトを UTC に変換して、 tzinfo を消します。

   :param datetime: ローカルタイムゾーンの datetime オブジェクト
   :param tzname: タイムゾーンの名前
   :return: UTC タイムゾーンの datetime.datetime オブジェクト

.. function:: get_by_key_name_or_404(model_class, key_name)

   与えられたキー名でデータを取得して返します。失敗したら :class:`werkzeug.exceptions.NotFound` をあげます。
   
   :param model_class: モデルクラス
   :param key_name:  model_class.get_by_key_name に渡すキー名
   :return: 成功した場合は、モデルクラスのインスタンス

.. function:: get_by_id_or_404(model_class, id)

   与えられた ID でデータを取得して返します。失敗したら :class:`werkzeug.exceptions.NotFound` をあげます。

   :param model_class: モデルクラス
   :param key_name:  model_class.get_by_key_id に渡す ID
   :return: 成功した場合は、モデルクラスのインスタンス

.. function:: get_or_404(model_class, key)

   与えられた キー でデータを取得して返します。失敗したら :class:`werkzeug.exceptions.NotFound` をあげます。

   :param model_class: モデルクラス
   :param key_name:  model_class.get に渡す キー
   :return: 成功した場合は、モデルクラスのインスタンス
