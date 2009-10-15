======================
リクエストオブジェクト
======================

概要
====

Kay のリクエストオブジェクトは、WSGI に準拠した Werkzeug のリクエストオブジェクトを採用しています。Kay は、ブラウザからアクセスされるとリクエストオブジェクトを生成し、URLマッピングによって特定したview関数に生成したリクエストオブジェクトを渡します。view関数は第１引数にリクエストオブジェクトをとり、レスポンスオブジェクトを生成して返します。ここでは、Kay のリクエストオブジェクト、および、レスポンス・オブジェクトの取り扱いについて説明します。


リクエスト・オブジェクト
========================


特徴
----

* デフォルトでは、リクエストオブジェクトは変更できません。
* リクエストオブジェクトはpickelできません。


属性
----

リクエストオブジェクトは以下の属性値を持っています。


* accept_charsets

  Accept-Charset リクエストヘッダフィールドです。

* accept_encodings

  Accept-Encodings リクエストヘッダフィールドです。

* accept_languages

  Accept-Languages リクエストヘッダフィールドです。

* accept_mimetypes

  Accept-Mimetipes リクエストヘッダフィールドです。

* access_route

  フォワードヘッダがある場合、クライアントのIPからサーバの直前のプロキシサーバまでのIPアドレスのリストが格納されます。
  
.. program:: manage.py add_translations

* application(f)

  関数を第１引数に受け取ったリクエストを受け取るレスポンダとしてデコレートできます。

   .. code-block:: python

   	  @Request.application
   	  def my_wsgi_app(request):
   	    return Response('Hello World!')

   引数： the WSGI callable to decorate

   戻り値：a new WSGI callable

* args

  URLパラメータがディクショナリで格納されます。

* authorization

  TODO

* base_url

  クエリ文字列を省いたURLです。

* cache_control

  キャッシュコントロールヘッダです。

* charset

  リクエストの文字セットです。デフォルト値は ``UTF-8`` です。

* content_length

  Content-Length エンティティヘッダフィールドは、受信者に送信されるエンティティボディのサイズを示します。HEAD メソッドの場合は GET リクエストされた場合に送信されるエンティティボディのサイズを示します。

* content_type

  Content-Type エンティティヘッダフィールドは、受信者に送信されるエンティティボディのメディアタイプを示します。HEADメソッドの場合、GET リクエストされた場合に送信されるエンティティボディのメディアタイプを示します。

* cookies

  ディクショナリとして、cookieの値を扱うことができます。

* data

  クライアントからのバッファされた入力データを文字列に読み込みます。通常これは ``data`` にアクセスするには悪いアイディアです。サーバのメモリに問題を引き起こすために、クライアントが何十メガバイトものデータを送ることができてしまうためです。

  これを回避するためには、 ``content_length`` を先にチェックしてください。

* date

  Date ジェネラルヘッダフィールドは、メッセージが生成された日付と時間を表します。RFC 822の orig-date と同じセマンティクスをもっています。

* encoding_errors

  エラーハンドリングプロシージャです。デフォルト値は ``ignore`` です。

* environ

  リクエストオブジェクトがデータを取り扱うためのWSGI environmentです。

* files

  アップロードされたすべてのファイルを格納した ``MultiDict`` オブジェクトです。 ``files`` のそれぞれのキーは ``<input type="file" name="">`` のnameです。それぞれの値は Werkzeug の ``FileStorage`` オブジェクトです。

  ``files`` は、リクエストメソッドが ``POST`` か、 ``PUT`` で、ポストされた ``<form>`` が ``enctype="multipart/form-data`` を持つ場合のみ、データを持ちます。そうでない場合は空です。

* form

  フォームのパラメータです。現在は、この関数が返すディクショナリの中身が、サブミットされたフォームデータと同じ順序であることは保証されていません。

  .. seealso:: :doc:`forms-usage`

* from_values(*args, **kwargs)

  提供された値をもとに、リクエストオブジェクトを新たに生成します。もし `environ` が与えられていれば、不足している値はそこから提供されます。URL からのリクエストをシミュレートする必要がある場合、簡単なスクリプトを書くのにはこのメソッドは便利です。ただし、このメソッドをユニットテストには使用しないでください。フルフィーチャーのクライアントオブジェクト( ``Client`` )があり、マルチパートのリクエストの生成、cookieのサポートなどが可能です。
  
* headers

  WSGI環境のヘッダです。不変の ``EnvironHeaders`` です。TODO

* host

  ホストです。取得可能ならポートもつきます。

* host_url

  スキームをもったホストです。TODO

* if_match

  If-Match ヘッダ中のすべてのetagsを格納したオブジェクトです。  

* if_modified_since

  パースされた ``If-Modified_Since`` ヘッダが ``datetime`` オブジェクトして格納されています。

* if_none_match

  ``If-Not-Match`` ヘッダ中のすべてのetagsを格納したオブジェクトです。  

* if_unmodified_since

  パースされた ``If-Unmodified_Since`` ヘッダが ``datetime`` オブジェクトして格納されています。
  
* input_stream

  TODO  

* is_behind_proxy

  HTTP プロキシの背後でアプリケーションが起動している場合に、 ``True`` となります。

* is_multiprocess

  複数のプロセスを生成しているWSGIサーバによってアプリケーションが提供されている場合、 ``True`` となります。

* is_multithread

  マルチスレッドの WSGI サーバによってアプリケーションが提供されている場合は ``True`` となります。

* is_run_once

  アプリケーションがプロセスの実行中に一度だけ実行される場合は、 ``True`` になります。これは、例えばCGIのような場合ですが、一度だけ実行されることは保証されていません。
  TODO

* is_secure

  セキュアなリクエストの場合、 ``True`` が格納されます。

* is_xhr

  リクエストが、JavaScript XMLHttpRequestを介して発行された場合、 ``True`` が格納されます。ライブラリが ``X-Requested-With`` ヘッダをサポートし、 ``XMLHttpRequest`` をセットしている場合のみ有効になります。prototype, jQuery, Mochikitなどが上記をサポートしています。

* lang

  ブラウザの言語設定です。

* max_content_length

  コンテント長の最大値です。これは、フォームデータのパース関数( ``parse_form_data`` )に渡されます。セットされて、 ``form`` や ``file`` 属性がアクセスされると、パースは失敗します。指示子が ``RequestEntityTooLarge`` エクセプションがあがり、を送信されるので
TODO

* max_form_memory_size

  TODO ほぼ同上

* max_forwards

  Max-Forwardsリクエストヘッダフィールドは、TRACEとOPTIONSメソッドに、リクエストを別のサーバへフォワードするプロキシやゲートウェアの数を制限する仕組みを提供します。

* method

  HTTPメソッドです。 ``GET`` or ``POST``

* mimetype

  ``content-type`` と似ていますが、パラメータ（例：文字セット、型など）がありません。例えば、コンテントタイプが ``text/html; charset=utf-8`` の場合、mimetypeは ``'text/html'`` となります。

* mimetype_params

  mimtypeパラメータがディクショナリで格納されています。例えば、コンテントタイプが ``text/html; charset=utf-8`` の場合、パラメータは ``{'charset': 'utf-8'}`` のようになっています。

* path

  リクエストされたパスがUnicodeで格納されます。WSGI環境のパスと同じようなものですが、常にスラッシュが含まれます。ルートへの対するアクセスでも同様です。

* pragma

  Pragmaジェネラルヘッダフィールドは、リクエスト/レスポンス連鎖中のあらゆる受信者にも適用されるであろう実装の特別な指示を示すために使われます。全ての pragma 指示子は、プロトコルの視点から見ればオプショナルな振る舞いを指定しますが、その振る舞いが指示子と一致していることを要求するシステムがあるかもしれません。
  

* query_string

  URLパラメータです。バイトストリングで格納されています。

* referrer

  Referer[原文ママ] リクエストヘッダフィールドは、サーバの利益のために、 Request-URI が取得されたリソースのアドレス (URI) をクライアントに示させます。

* remote_addr

  クライアントのリモートアドレスです。

* remote_user

  ユーザ認証を有効にしている場合、ユーザ名が格納されます。

* script_root

  末尾のスラッシュを取り除いた、スクリプトのルートパスです。

* session

  セッションデータが格納されています。セッション機能を有効にすると使用できます。

  .. seealso:: :doc:`session`

* shallow

  リクエストがenvironのshallow copyである場合、 ``True`` が格納されています。

* stream

  もしサブミットされたデータが複数のパートをもたないか、urlエンコードされたフォームデータでなければ、パースされたストリームが格納されます。このストリームはパースされた後に、フォームデータパーサモジュールによって残されたストリームです。TODO

* url

  リモートアドレスです。

* url_charset

  URLに使われる文字セットです。デフォルトは ``charset`` の値になっています。

* url_root

  ホストネームのついた完全なURLです。これはアプリケーションルートです。

* user

  ユーザ認証を有効にしている場合、 ``settings.py`` の ``AUTH_USER_MODEL`` で指定したユーザオブジェクトが格納されます。

  .. seealso:: :doc:`auth`

* user_agent

  現在のユーザエージェントです。

* values

  ``args`` や ``form`` のための、ディクショナリです。


メソッド
--------

* _get_file_stream(total_content_length, content_type, filename=None, content_length=None)



* _form_parsing_failed(error)


クラスメソッド
--------------

* application(f)


 
* from_values(*args, **kwargs)



* GETのパラメータ取得するには、以下のように記述します。

.. code-block:: python

   request.GET["param"]




レスポンスオブジェクト
======================



属性
----

* data

  リクエスト本文の文字列です。この属性にアクセスするときは、リクエストはイテラブルはエンコードされ平板化されています。これは、ストリームが巨大なデータである場合に、不測の振る舞いを引き起こす可能性があります。

  TODO


Werkzeug

.. seealso:: http://werkzeug.pocoo.org/documentation/dev/wrappers.html


