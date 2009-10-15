==============================================
リクエストオブジェクトとレスポンスオブジェクト
==============================================

概要
====

Kay は、WSGI に準拠した Werkzeug のリクエストオブジェクト、および、レスポンスオブジェクトを採用しています。Kay は、ブラウザからアクセスされるとリクエストオブジェクトを生成し、URLマッピングによって特定したview関数に渡します。view関数は第１引数にリクエストオブジェクトをとり、レスポンスオブジェクトを生成して返す必要があります。ここでは、リクエストオブジェクト、および、レスポンスオブジェクトの構成について説明します。


リクエストオブジェクト
======================


特徴
----

* view関数は、リクエストオブジェクトを引数にとります。
* リクエストオブジェクトは読み込みのみ可能です。変更は許可されていません。
* デフォルトでは、リクエストオブジェクトのテキストデータはすべて ``UTF-8`` でエンコードされています。


属性
----

リクエストオブジェクトは以下の属性値を持っています。

.. attribute:: accept_charsets

   Accept-Charset リクエストヘッダフィールドです。

.. attribute:: accept_encodings

   Accept-Encodings リクエストヘッダフィールドです。

.. attribute:: accept_languages

   Accept-Languages リクエストヘッダフィールドです。

.. attribute:: accept_mimetypes

   Accept-Mimetipes リクエストヘッダフィールドです。

.. attribute:: access_route

   フォワードヘッダがある場合、クライアントのIPからサーバの直前のプロキシサーバまでのIPアドレスのリストが格納されます。
  
.. classmethod:: application(f)

   関数を第１引数に受け取ったリクエストを受け取るレスポンダとしてデコレートできます。

   .. code-block:: python

   	  @Request.application
	  def my_wsgi_app(request):
   	  	  return Response('Hello World!')

   :param f: the WSGI callable to decorate
   :rtype: a new WSGI callable


.. attribute:: args

  URLパラメータがディクショナリで格納されます。

.. attribute:: authorization

  TODO

.. attribute:: base_url

  クエリ文字列を省いたURLです。

.. attribute:: cache_control

  キャッシュコントロールヘッダです。

.. attribute:: charset

  リクエストの文字セットです。デフォルト値は ``UTF-8`` です。

.. attribute:: content_length

  Content-Length エンティティヘッダフィールドは、受信者に送信されるエンティティボディのサイズを示します。HEAD メソッドの場合は GET リクエストされた場合に送信されるエンティティボディのサイズを示します。

.. attribute:: content_type

  Content-Type エンティティヘッダフィールドは、受信者に送信されるエンティティボディのメディアタイプを示します。HEADメソッドの場合、GET リクエストされた場合に送信されるエンティティボディのメディアタイプを示します。

.. attribute:: cookies

  ディクショナリとして、cookieの値を扱うことができます。

.. attribute:: data

  クライアントからのバッファされた入力データを文字列に読み込みます。通常これは ``data`` にアクセスするには悪いアイディアです。サーバのメモリに問題を引き起こすために、クライアントが何十メガバイトものデータを送ることができてしまうためです。

  これを回避するためには、 ``content_length`` を先にチェックしてください。

.. attribute:: date

  Date ジェネラルヘッダフィールドは、メッセージが生成された日付と時間を表します。RFC 822の orig-date と同じセマンティクスをもっています。

.. attribute:: encoding_errors

  エラーハンドリングプロシージャです。デフォルト値は ``ignore`` です。

.. attribute:: environ

  リクエストオブジェクトがデータを取り扱うためのWSGI environmentです。

.. attribute:: files

  アップロードされたすべてのファイルを格納した ``MultiDict`` オブジェクトです。 ``files`` のそれぞれのキーは ``<input type="file" name="">`` のnameです。それぞれの値は Werkzeug の ``FileStorage`` オブジェクトです。

  ``files`` は、リクエストメソッドが ``POST`` か、 ``PUT`` で、ポストされた ``<form>`` が ``enctype="multipart/form-data`` を持つ場合のみ、データを持ちます。そうでない場合は空です。

.. attribute:: form

  フォームのパラメータです。現在は、この関数が返すディクショナリの中身が、サブミットされたフォームデータと同じ順序であることは保証されていません。

  .. seealso:: :doc:`forms-usage`

.. attribute:: from_values(*args, **kwargs)

  提供された値をもとに、リクエストオブジェクトを新たに生成します。もし `environ` が与えられていれば、不足している値はそこから提供されます。URL からのリクエストをシミュレートする必要がある場合、簡単なスクリプトを書くのにはこのメソッドは便利です。ただし、このメソッドをユニットテストには使用しないでください。フルフィーチャーのクライアントオブジェクト( ``Client`` )があり、マルチパートのリクエストの生成、cookieのサポートなどが可能です。
  
.. attribute:: headers

  WSGI環境のヘッダです。不変の ``EnvironHeaders`` です。TODO

.. attribute:: host

  ホストです。取得可能ならポートもつきます。

.. attribute:: host_url

  スキームをもったホストです。TODO

.. attribute:: if_match

  If-Match ヘッダ中のすべてのetagsを格納したオブジェクトです。  

.. attribute:: if_modified_since

  パースされた ``If-Modified_Since`` ヘッダが ``datetime`` オブジェクトして格納されています。

.. attribute:: if_none_match

  ``If-Not-Match`` ヘッダ中のすべてのetagsを格納したオブジェクトです。  

.. attribute:: if_unmodified_since

  パースされた ``If-Unmodified_Since`` ヘッダが ``datetime`` オブジェクトして格納されています。
  
.. attribute:: input_stream

  TODO  

.. attribute:: is_behind_proxy

  HTTP プロキシの背後でアプリケーションが起動している場合に、 ``True`` となります。

.. attribute:: is_multiprocess

  複数のプロセスを生成しているWSGIサーバによってアプリケーションが提供されている場合、 ``True`` となります。

.. attribute:: is_multithread

  マルチスレッドの WSGI サーバによってアプリケーションが提供されている場合は ``True`` となります。

.. attribute:: is_run_once

  アプリケーションがプロセスの実行中に一度だけ実行される場合は、 ``True`` になります。これは、例えばCGIのような場合ですが、一度だけ実行されることは保証されていません。
  TODO

.. attribute:: is_secure

  セキュアなリクエストの場合、 ``True`` が格納されます。

.. attribute:: is_xhr

  リクエストが、JavaScript XMLHttpRequestを介して発行された場合、 ``True`` が格納されます。ライブラリが ``X-Requested-With`` ヘッダをサポートし、 ``XMLHttpRequest`` をセットしている場合のみ有効になります。prototype, jQuery, Mochikitなどが上記をサポートしています。

.. attribute:: lang

  ブラウザの言語設定です。

.. attribute:: max_content_length

  コンテント長の最大値です。これは、フォームデータのパース関数( ``parse_form_data`` )に渡されます。セットされて、 ``form`` や ``file`` 属性がアクセスされると、パースは失敗します。指示子が ``RequestEntityTooLarge`` エクセプションがあがり、を送信されるので
TODO

.. attribute:: max_form_memory_size

  TODO ほぼ同上

.. attribute:: max_forwards

  Max-Forwards リクエストヘッダフィールドは、 TRACE と OPTIONS メソッドに、リクエストを別のサーバへフォワードするプロキシやゲートウェアの数を制限する仕組みを提供します。

.. attribute:: method

  HTTPメソッドです。 ``GET`` or ``POST``

.. attribute:: mimetype

  ``content-type`` と似ていますが、パラメータ（例：文字セット、型など）がありません。例えば、コンテントタイプが ``text/html; charset=utf-8`` の場合、mimetypeは ``'text/html'`` となります。

.. attribute:: mimetype_params

  mimtypeパラメータがディクショナリで格納されています。例えば、コンテントタイプが ``text/html; charset=utf-8`` の場合、パラメータは ``{'charset': 'utf-8'}`` のようになっています。

.. attribute:: path

  リクエストされたパスがUnicodeで格納されます。WSGI環境のパスと同じようなものですが、常にスラッシュが含まれます。ルートへの対するアクセスでも同様です。

.. attribute:: pragma

  Pragmaジェネラルヘッダフィールドは、リクエスト/レスポンス連鎖中のあらゆる受信者にも適用されるであろう実装の特別な指示を示すために使われます。全ての pragma 指示子は、プロトコルの視点から見ればオプショナルな振る舞いを指定しますが、その振る舞いが指示子と一致していることを要求するシステムがあるかもしれません。
  

.. attribute:: query_string

  URLパラメータです。バイトストリングで格納されています。

.. attribute:: referrer

  Referer[原文ママ] リクエストヘッダフィールドは、サーバの利益のために、 Request-URI が取得されたリソースのアドレス (URI) をクライアントに示させます。

.. attribute:: remote_addr

  クライアントのリモートアドレスです。

.. attribute:: remote_user

  ユーザ認証を有効にしている場合、ユーザ名が格納されます。

.. attribute:: script_root

  末尾のスラッシュを取り除いた、スクリプトのルートパスです。

.. attribute:: session

  セッションデータが格納されています。セッション機能を有効にすると使用できます。

  .. seealso:: :doc:`session`

.. attribute:: shallow

  リクエストがenvironのshallow copyである場合、 ``True`` が格納されています。

.. attribute:: stream

  もしサブミットされたデータが複数のパートをもたないか、urlエンコードされたフォームデータでなければ、パースされたストリームが格納されます。このストリームはパースされた後に、フォームデータパーサモジュールによって残されたストリームです。TODO

.. attribute:: url

  リモートアドレスです。

.. attribute:: url_charset

  URLに使われる文字セットです。デフォルトは ``charset`` の値になっています。

.. attribute:: url_root

  ホストネームのついた完全なURLです。これはアプリケーションルートです。

.. attribute:: user

  ユーザ認証を有効にしている場合、 ``settings.py`` の ``AUTH_USER_MODEL`` で指定したユーザオブジェクトが格納されます。

  .. seealso:: :doc:`auth`

.. attribute:: user_agent

  現在のユーザエージェントです。

.. attribute:: values

  ``args`` や ``form`` のための、ディクショナリです。


メソッド
--------

.. attribute:: _get_file_stream(total_content_length, content_type, filename=None, content_length=None)



.. attribute:: _form_parsing_failed(error)


クラスメソッド
--------------

.. classmethod:: application(f)


 
.. classmethod:: from_values(*args, **kwargs)




パラメータの取得
----------------

* GETのパラメータ取得するには、以下のように記述します。

.. code-block:: python

   request.GET["param"]


レスポンスオブジェクト
======================

view関数は、必ずレスポンスオブジェクトを返す必要があります。レスポンスオブジェクトは ``Response`` クラスのインスタンスです。html


属性
----

レスポンスオブジェクトは以下の属性値を持っています。

.. attribute:: _get_mimetype_params
.. attribute:: add_etag(overwrite=False, weak=False)
  
.. attribute:: age
.. attribute:: allow
.. attribute:: cache_control
.. attribute:: charset

  レスポンスの文字セットです。

.. attribute:: close()

  可能であれば、ラップされたレスポンスをクローズします。

.. attribute:: content_encoding
.. attribute:: content_language
.. attribute:: content_length
.. attribute:: content_location
.. attribute:: content_md5
.. attribute:: content_type

  Content-Type エンティティヘッダフィールドは、受信者に送信されるエンティティボディのメディアタイプを示します。HEADメソッドの場合、GET リクエストされた場合に送信されるエンティティボディのメディアタイプを示します。

.. attribute:: data

  リクエスト本文の文字列です。この属性にアクセスするときは、リクエストはイテラブルはエンコードされ平板化されています。これは、ストリームが巨大なデータである場合に、不測の振る舞いを引き起こす可能性があります。

  TODO

.. attribute:: date

  Date ジェネラルヘッダフィールドは、メッセージが生成された日付と時間を表します。RFC 822の orig-date と同じセマンティクスをもっています。

.. attribute:: default_mimetype

  mimetype が設定されていない場合のデフォルトの mimetype です。

.. attribute:: default_status

  status が設定されていない場合のデフォルトの status です。

.. attribute:: direct_passthrough

  もし、WSGI アプリケーションとしてのレスポンスオブジェクトが使用される前に、 ``direct_passthrough=True`` がレスポンスオブジェクトに渡されるか、この属性が ``True`` にセットされるかしたた場合、イテレータは変更なしで返されます。これによって、特別な ``wsgi.file_wrapper`` をレスポンスオブジェクトに渡すことができます。詳しくは ``wrap_file()`` を参照してください。

  TODO

.. attribute:: expires

  

.. attribute:: fix_headers
.. attribute:: get_app_iter
.. attribute:: get_etag
.. attribute:: get_wsgi_headers
.. attribute:: get_wsgi_response
.. attribute:: header_list
.. attribute:: headers

  レスポンスヘッダを表す ``Headers`` オブジェクトです。

.. attribute:: is_streamed
.. attribute:: last_modified
.. attribute:: location
.. attribute:: make_conditional
.. attribute:: mimetype

  ``content-type`` と似ていますが、パラメータ（例：文字セット、型など）がありません。例えば、コンテントタイプが ``text/html; charset=utf-8`` の場合、mimetypeは ``'text/html'`` となります。

.. attribute:: mimetype_params

  mimtypeパラメータがディクショナリで格納されています。例えば、コンテントタイプが ``text/html; charset=utf-8`` の場合、パラメータは ``{'charset': 'utf-8'}`` のようになっています。

.. attribute:: response

  アプリケーションイテレータです。文字列で構成されていればリストになり、それ以外では、アプリケーションイテレータとして提供されます。

.. attribute:: retry_after

  

.. attribute:: set_etag
.. attribute:: status

  文字列のステータスか、整数値のステータスコードを渡します。

.. attribute:: status_code

  レスポンスステータスです。整数値です。

.. attribute:: stream
.. attribute:: vary
.. attribute:: www_authenticate



メソッド
--------

* delete_cookie(key, path='/', domain=None)

  cookie を削除します。

* force_type()

* freeze()

  pickleされるレスポンスオブジェクトを作成する場合は、このメソッドを呼び出してください。

  TODO

* from_app(app, environ, buffered=False)
* iter_encoded
* set_cookie


生成方法
--------

レスポンスオブジェクトは、 ``werkzeug.Response`` クラスのインスタンスです。Kay には、レスポンスを生成するための関数が用意されています。


.. function:: render_to_response(template, context, mimetype='text/html', processors=None)

   HTMLページのレンダリング

   :param template: テンプレート
   :param context: コンテキスト
   :param mimetype: mimetype
   :param processors: コンテキストプロセッサ
   :rtype: レスポンスオブジェクト

.. function:: render_error(e)

   エラーページのレンダリング

   :param e: エクセプションオブジェクト
   :rtype: レスポンスオブジェクト



   
.. seealso:: http://werkzeug.pocoo.org/documentation/dev/wrappers.html


