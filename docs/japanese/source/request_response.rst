==============================================
リクエストオブジェクトとレスポンスオブジェクト
==============================================

概要
====

Kay は、WSGI に準拠した Werkzeug のリクエストオブジェクト、および、レスポンスオブジェクトを採用しています。Kay は、ブラウザからアクセスされるとリクエストオブジェクトを生成し、URL マッピングによって特定した view 関数に渡します。 view 関数は第１引数にリクエストオブジェクトをとり、レスポンスオブジェクトを生成して返す必要があります。ここでは、リクエストオブジェクト、および、レスポンスオブジェクトの構成について説明します。

.. currentmodule:: werkzeug

リクエストオブジェクト
======================

* view は、リクエストオブジェクトを引数にとります。
* リクエストオブジェクトは読み込み専用です。変更は許可されていません。
* デフォルトでは、リクエストオブジェクトのテキストデータはすべて ``UTF-8`` でエンコードされています。


属性とメソッド
--------------

リクエストオブジェクトは以下の属性を持っています。

.. class:: Request

  .. attribute:: accept_charsets

     クライアントがサポートしている文字セットのリストです。 `CharsetAccept <http://werkzeug.pocoo.org/documentation/0.5.1/datastructures.html#werkzeug.CharsetAccept>`_ オブジェクトとして提供されます。

  .. attribute:: accept_encodings

     クライアントが許容しているエンコーディングのリストです。HTTP の用語において、gzipのようなエンコーディングの圧縮です。 文字セットについては ``accept_charsets`` を参照して下さい。

  .. attribute:: accept_languages

     クライアントが許容している言語のリストです。 `LanguageAccept <http://werkzeug.pocoo.org/documentation/0.5.1/datastructures.html#werkzeug.LanguageAccept>`_ オブジェクトとして提供されます。

  .. attribute:: accept_mimetypes

     クライアントがサポートしている mimetype のリストです。 `MIMEAccept <http://werkzeug.pocoo.org/documentation/0.5.1/datastructures.html#werkzeug.MIMEAccept>`_ オブジェクトとして提供されます。

  .. attribute:: access_route

     フォワードヘッダがある場合、クライアントのIPからサーバの直前のプロキシサーバまでのIPアドレスのリストが格納されます。
  
  .. attribute:: args

     パースされたURLパラメータです。 `ImmutableMultiDict <http://werkzeug.pocoo.org/documentation/0.5.1/datastructures.html#werkzeug.ImmutableMultiDict>`_ に格納されます。

  .. attribute:: authorization

     パースされたフォームの中の ``Authorization`` オブジェクトです。

  .. attribute:: base_url

     ``url`` と似ていますが、クエリ文字列が省かれています。

  .. attribute:: cache_control

     受信したキャッシュコントロールヘッダを `RequestCacheControl <http://werkzeug.pocoo.org/documentation/0.5.1/datastructures.html#werkzeug.RequestCacheControl>`_ オブジェクトとして提供します。

  .. attribute:: charset

     リクエストの文字セットです。デフォルト値は ``UTF-8`` です。

  .. attribute:: content_length

     Content-Length エンティティヘッダフィールドは、受信者に送信されるエンティティボディのサイズを示します。HEAD メソッドの場合は GET リクエストされた場合に送信されるエンティティボディのサイズを示します。

  .. attribute:: content_type

     Content-Type エンティティヘッダフィールドは、受信者に送信されるエンティティボディのメディアタイプを示します。HEADメソッドの場合、GET リクエストされた場合に送信されるエンティティボディのメディアタイプを示します。

  .. attribute:: cookies

     ディクショナリとして、cookieの値を扱うことができます。

  .. attribute:: data

     バッファリングされたクライアントからの入力データを文字列に読み込みます。普通は ``data`` にアクセスする方法としてはよくない方法です。クライアントが、サーバのメモリを浪費させるために、何十メガバイトものデータを送ることができてしまうためです。

     これを避けるには、 ``content_length`` を先にチェックしてください。

  .. attribute:: date

     Date ジェネラルヘッダフィールドは、メッセージが生成された日付と時間を表します。RFC 822の orig-date と同じセマンティクスをもっています。

  .. attribute:: encoding_errors

     エラーハンドリングプロシージャです。デフォルト値は ``ignore`` です。

  .. attribute:: environ

     リクエストオブジェクトがデータを取り扱うための WSGI env です。

  .. attribute:: files

     アップロードされたすべてのファイルを格納した ``MultiDict`` オブジェクトです。 ``files`` のそれぞれのキーは ``<input type="file" name="">`` のnameです。それぞれの値は Werkzeug の ``FileStorage`` オブジェクトです。

     ``files`` は、リクエストメソッドが ``POST`` か ``PUT`` で、ポストされた ``<form>`` が ``enctype="multipart/form-data"`` を持つ場合のみデータを持ちます。そうでない場合は空です。

  .. attribute:: form

     フォームのパラメータです。現状、この関数が返すディクショナリの中身がサブミットされたフォームデータと同じ順序かどうかは保証されていません。

   
     .. seealso:: :doc:`forms-usage`

   
  .. classmethod:: from_values(*args, **kwargs)

     提供された値をもとに、リクエストオブジェクトを新たに生成します。も
     し `environ` が与えられていれば、不足している値はそこから提供され
     ます。URL からのリクエストをシミュレートする必要がある場合、簡単な
     スクリプトを書くのにはこのメソッドは便利です。ただし、このメソッド
     をユニットテストには使用しないでください。フル機能のクライアントオ
     ブジェクト( ``Client`` )があり、マルチパートのリクエストの生成、
     cookie のサポートなどが可能です。
  
  .. attribute:: headers

     WSGI env 由来のヘッダです。変更不可の `EnvironHeaders <http://werkzeug.pocoo.org/documentation/0.5.1/datastructures.html#werkzeug.EnvironHeaders>`_ です。

  .. attribute:: host

     ホストです。取得可能であればポートも含みます。

  .. attribute:: host_url

     スキーム名つきのホストです。

  .. attribute:: if_match

     If-Match ヘッダ中のすべてのetags を格納したオブジェクトです。  

  .. attribute:: if_modified_since

     パースされた ``If-Modified_Since`` ヘッダが ``datetime`` オブジェクトして格納されています。

  .. attribute:: if_none_match

     ``If-None-Match`` ヘッダ中のすべてのetagsを格納したオブジェクトです。  

  .. attribute:: if_unmodified_since

     パースされた ``If-Unmodified_Since`` ヘッダが ``datetime`` オブジェクトして格納されています。
  
  .. attribute:: is_behind_proxy

     HTTP プロキシの後ろでアプリケーションが起動している場合に ``True`` となります。

  .. attribute:: is_multiprocess

     複数のプロセスを生成している WSGI サーバによってアプリケーションが提供されている場合に ``True`` となるブール値です。

  .. attribute:: is_multithread

     マルチスレッドの WSGI サーバによってアプリケーションが提供されている場合に ``True`` となるブール値です。

  .. attribute:: is_run_once

     アプリケーションがプロセスの生存期間中に一度だけ実行であろう場合は ``True`` になるブール値です。例えば CGI のような場合にあたりますが、一度だけ実行されることは保証されていません。

  .. attribute:: is_secure

     セキュアなリクエストの場合 ``True`` となります。

  .. attribute:: is_xhr

     リクエストが JavaScript XMLHttpRequest を介して発行された場合、 ``True`` になります。ライブラリが ``X-Requested-With`` ヘッダをサポートし、 ``XMLHttpRequest`` をセットしている場合のみ機能します。prototype, jQuery, Mochikitなどが上記をサポートしています。

  .. attribute:: lang

     リクエストから Kay が推測した結果の使用言語が格納されています。

  .. attribute:: max_content_length

     コンテント長の最大値です。この値はフォームデータをパースする関数( `parse_form_data() <http://werkzeug.pocoo.org/documentation/dev/http.html#werkzeug.parse_form_data>`_ )に渡されます。値がセットされていて、 ``form`` や ``file`` 属性にアクセスされ、指定した値を超える転送があってパースが失敗する場合、 `RequestEntityTooLarge <http://werkzeug.pocoo.org/documentation/dev/exceptions.html#werkzeug.exceptions.RequestEntityTooLarge>`_ エクセプションがあがります。

  .. attribute:: max_form_memory_size

     フォームフィールドの最大サイズです。この値はフォームデータをパースする関数( `parse_form_data() <http://werkzeug.pocoo.org/documentation/dev/http.html#werkzeug.parse_form_data>`_ )に渡されます。値がセットされていて、 ``form`` や ``file`` 属性にアクセスされ、ポストデータ用のメモリーデータが指定した値を超えると、 `RequestEntityTooLarge <http://werkzeug.pocoo.org/documentation/dev/exceptions.html#werkzeug.exceptions.RequestEntityTooLarge>`_ エクセプションがあがります。

  .. attribute:: max_forwards

     Max-Forwards リクエストヘッダフィールドは、 TRACE と OPTIONS メソッドに、リクエストを別のサーバへフォワードするプロキシやゲートウェイの数を制限する仕組みを提供します。

  .. attribute:: method

     HTTPメソッドです。 ``GET``  ``POST`` などです。

  .. attribute:: mimetype

     ``content-type`` と似ていますが、パラメータ（例：文字セット、型など）がありません。例えば、コンテントタイプが ``text/html; charset=utf-8`` の場合、mimetypeは ``'text/html'`` となります。

  .. attribute:: mimetype_params

     mimetypeパラメータがディクショナリで格納されています。例えば、コンテントタイプが ``text/html; charset=utf-8`` の場合、パラメータは ``{'charset': 'utf-8'}`` のようになっています。

  .. attribute:: path

    リクエストされたパスがUnicodeで格納されます。WSGI env のパスと同じようなものですが、常にスラッシュが含まれます。ルートへの対するアクセスでも同様です。

  .. attribute:: pragma

     Pragma ジェネラルヘッダフィールドは、リクエスト/レスポンス連鎖中のあらゆる受信者にも適用されるであろう実装の特別な指示を示すために使われます。全ての pragma 指示子は、プロトコルの視点から見ればオプショナルな振る舞いを指定しますが、その振る舞いが指示子と一致していることを要求するシステムがあるかもしれません。
  

  .. attribute:: query_string

     URL パラメータです。バイトストリングで格納されています。

  .. attribute:: referrer

     Referrer です。

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

     もしサブミットされたデータがマルチパートでないか、 url エンコードされたフォームデータでない場合、パースされたストリームが格納されます。このストリームはフォームデータパーサモジュールがパース後に残したストリームです。これは、 WSGI インプットストリームそのものではなく、呼び出し元が ``Content-Length`` を読み込まない危険性を避けるため、ストリームのラッパを返します。

  .. attribute:: url

     URL です。

  .. attribute:: url_charset

     URL に使われる文字セットです。デフォルトは ``charset`` の値になっています。

  .. attribute:: url_root

     ホストネームのついた完全な URL です。これはアプリケーションルートです。

  .. attribute:: user

     ユーザ認証を有効にしている場合、 ``settings.py`` の ``AUTH_USER_MODEL`` で指定したユーザオブジェクトが格納されます。

   
     .. seealso:: :doc:`auth`

  .. attribute:: user_agent

     現在のユーザエージェントです。

  .. attribute:: values

     ``args``  ``form`` 両方を結合したディクショナリと考えてください。


レスポンスオブジェクト
======================

* view は、必ずレスポンスオブジェクトを返す必要があります。
* レスポンスオブジェクトはに対して、 ``freeze()`` を呼び出すと、pickleや、コピーができます。
* copy.deepcopy によって、コピーを作成することはできません。

属性とメソッド
--------------

レスポンスオブジェクトは以下の属性、および、メソッドを持っています。

.. class:: Response

  .. method:: add_etag(overwrite=False, weak=False)

     現在のオブジェクトに etag を追加します。   

  .. attribute:: age
   
     Age レスポンスヘッダは、オリジンサーバにおいてレスポンス（または、その再検証が) が生成されてからの、送信者の推定経過時間を示します。

     Age の値は、負値でない10進数の整数で、秒で時間を表します。

  .. attribute:: allow

     Allow エンティティヘッダフィールドは、 Request-URI によって識別されたリソースによってサポートされているメソッドのセットを示します。このフィールドの目的は、リソースに関する有効なメソッドを受信者に厳密に知らせることです。Allow ヘッダは 405 (Method Not Allowed) レスポンス中に存在しなければなりません。

  .. attribute:: cache_control

     Cache-Control ジェネラルヘッダフィールドは、リクエスト/レスポンス連鎖の間のすべてのキャッシングメカニズムが従わなければならない指示を記述するために使用されます。

  .. attribute:: charset

     レスポンスの文字セットです。

  .. method:: close()

     レスポンスオブジェクトを pickle する際に、呼び出します。

  .. attribute:: content_encoding

     Content-Encoding エンティティヘッダフィールドは、メディアタイプの修飾子として使用されます。その値はどのコンテンツエンコーディングが追加で、エンティティボディに適用されているか、そしてその結果、 Content-Type ヘッダフィールドによって参照されるメディアタイプを取得するのためには、どのデコーディングメカニズムが適用されなければならないのかを示します。

  .. attribute:: content_language

     Content-Language エンティティヘッダフィールドは、付随するエンティティの読者の自然言語を表します。ただし、エンティティボディで使われている言語全部とは一致しないかもしれないので気をつけてください。

  .. attribute:: content_length

     Content-Length エンティティヘッダフィールドは、受信者に送信されるエンティティボディのサイズを8ビットの10進数で示します。HEAD メソッドの場合は GET リクエストされた場合に送信されるエンティティボディのサイズを示します。

  .. attribute:: content_location

     Content-Location エンティティヘッダフィールドは、エンティティがリクエストされたリソースの URI とは別の場所から取得可能な場合に、そのメッセージに含まれるエンティティに対するリソースの場所を与えるために使うことができます。

  .. attribute:: content_md5

     Content-MD5 エンティティヘッダフィールド (RFC 1864 に定義) は、エンティティボディのエンド・トゥ・エンドメッセージインテグリティチェック (MIC) を提供するためのエンティティボディの MD5 ダイジェストです。(注意： MIC は転送中のエンティティボディの偶発的な書き換えを発見するのには適していますが、悪意ある攻撃への対抗手段にはなりません）

  .. attribute:: content_type

     Content-Type エンティティヘッダフィールドは、受信者に送信されるエンティティボディのメディアタイプを示します。HEAD メソッドの場合、GET リクエストされた場合に送信されるエンティティボディのメディアタイプを示します。

  .. attribute:: data

     リクエスト本文の文字列を表します。この属性にアクセスするときはいつでもリクエストイテラブルはエンコードされフラット化されています。ストリームが巨大なデータである場合に、不測の振る舞いを引き起こす可能性があります。

  .. attribute:: date

     Date ジェネラルヘッダフィールドは、メッセージが生成された日付と時間を表します。RFC 822の orig-date と同じセマンティクスをもっています。

  .. attribute:: default_mimetype

     mimetype が設定されていない場合のデフォルトの mimetype です。

  .. attribute:: default_status

     status が設定されていない場合のデフォルトの status です。

  .. method:: delete_cookie(key, path='/', domain=None)

     cookie を削除します。キーがない場合は、フェールサイレントです。

     :param key: 削除される cookie のキー(名称)です。
     :param path: もし削除されるべき cookie があるパスに限定されている場合、そのパスを指定しなければなりません。
     :param domain: もし削除されるべき cookie があるドメインに限定されている場合、そのドメインを指定しなければなりません。

  .. attribute:: direct_passthrough

     もし、レスポンスオブジェクトが WSGI アプリケーションとして使用される前に ``direct_passthrough=True`` がレスポンスオブジェクトに渡されるか、あるいは、この属性が ``True`` にセットされるかした場合、ラップされたイテレータは変更なしで返されます。これによって、特別な ``wsgi.file_wrapper`` をレスポンスオブジェクトに渡すことができます。詳しくは `wrap_file() <http://werkzeug.pocoo.org/documentation/dev/wsgi.html#werkzeug.wrap_file>`_ を参照してください。

  .. attribute:: expires

     Expire エンティティヘッダフィールドはレスポンスが古くなると見なされる時点の日付と時間を表します。通常、キャッシュは、古いキャッシュエントリを返さないでしょう。

  .. method:: fix_headers(environ)

     レスポンスの開始の直前に自動的に呼び出され、ヘッダのよくある間違いを修正します。例えば、ロケーションヘッダはルートURLと結合されます。

     :param envirion: 修正の適用に使われるリクエストのWSGI env

  .. classmethod:: force_type(response, environ=None)

     WSGI レスポンスが現在の型のレスポンスオブジェクトであることを強制します。Werkzeug はエクセプションのような多くのシチュエーションで内部的には ``BaseResponse`` を使います。もしエクセプションに ``get_response`` を呼ぶのであれば、たとえ、カスタムサブクラスを使っていたとしても、通常の ``BaseResponse`` オブジェクトを返されるでしょう。

     このメソッドは与えられるレスポンスの型を強制できます。また、 envrion が与えると、WSGI 呼び出し可能オブジェクトを任意のレスポンスオブジェクトにコンバートします。

     これは、メインディスパッチャでレスポンスをポストプロセスし、サブクラスによって提供される機能を使いたい場合に特に有用です。

     可能な限り適切にレスポンスオブジェクトを変更することを覚えておいてください。

     :param response: レスポンスオブジェクト、または、WSGI アプリケーション
     :param environ: WSGI env オブジェクト
   
   
  .. classmethod:: from_app(app, environ, buffered=False)

     アプリケーションの出力から新しいレスポンスオブジェクトを作成します。これは、常にジェネレータを返すアプリケーションで呼び出すとうまくいきます。アプリケーションは ``start_response`` 関数が返す ``write()`` 呼び出し可能オブジェクトを使うかもしれません。このメソッドはそのようなケースを自動的に解決しようとします。しかし、期待した出力を得られない場合は、 ``buffered`` に ``True`` をセットしバッファリングを強制すべきです。

     :param app: 実行される WSGI アプリケーションです。
     :param environ: 再実行される WSGI env です。
     :param buffered: バッファリングを強制するには ``True`` をセットします。
     :rtype: レスポンスオブジェクト
   
  .. method:: get_app_iter(environ)

     与えられた environ に対するアプリケーションイテレータを返します。リクエストメソッドと現在のステータスコード次第で、戻り値は空のレスポンスになるでしょう。

     もし、リクエストメソッドが ``HEAD`` であるか、または、ステータスコードが HTTP の仕様が空のレスポンスを要求する範囲である場合は、空のイテラブルが返されます。

     :param environ: リクエストの WSGI env です。
     :rtype: レスポンスイテラブルです。
   
  .. method:: get_etag()

     ``(etag, is_weak)`` の形式のタプルを返します。　ETag がない場合は、戻り値は ``(None, None)`` です。
   
  .. method:: get_wsgi_headers(environ)

     このメソッドは、レスポンスが開始される直前に自動的に呼び出され、与えられた環境用に修正したヘッダを返します。必要であれば、いくつかの修正を適用してレスポンスからヘッダのコピーを返します。

     例えば、ロケーションヘッダ（もしあれば）は環境のルートURLと結合されます。また、ステータスコードによってはコンテンツ長は自動的に0がセットされます。

     :param envrion: リクエストの WSGI env です。
     :rtype: 新しいヘッダオブジェクトを返します。
   
  .. method:: get_wsgi_response(environ)

     最終的な WSGI レスポンスをタプルで返します。タプルの最初の項目はアプリケーションイテレータです。２番目はステータスで、３番目はリストのヘッダです。返されたレスポンスは与えられた環境向けに作られます。例えば、 WSGI envのリクエストメソッドが ``HEAD`` である場合、レスポンスは空になり、ヘッダとステータスコードだけがあるでしょう。

     :param environ: リクエストの WSGI env です。
     :rtype: アプリケーションイテレータ、ステータス、ヘッダのタプルです。
   
  .. attribute:: headers

     レスポンスヘッダを表す ``Headers`` オブジェクトです。

  .. attribute:: is_streamed

     もし、レスポンスがストリームの場合（レスポンスが長さの情報をもったイテラブルでない場合）、この属性は ``True`` になります。この場合、streamd はイテレーションの数についての情報を持たないということを意味します。ジェネレータがレスポンスオブジェクトに引き継がれる場合、通常 ``True`` になります。

  .. method:: iter_encoded(charset=None)

     指定されたエンコーディングでエンコードされたレスポンスのイテレータを返します。エンコーディングが指定されていない場合、クラスのエンコーディングが使われます。バイトストリングデータはエンコードされないことに注意してください。もしレスポンスオブジェクトが WSGI アプリケーションとして呼び出される場合、このメソッドの戻り値は ``direct_passthrough`` が有効な場合をのぞき、アプリケーションイテレータとして使用されます。

  .. attribute:: last_modified

     Last-Modified エンティティヘッダフィールドは、オリジンサーバーがバリアントが最後に更新されたと考える日付と時間を表します。

  .. attribute:: location

     Location レスポンスヘッダフィールドは、リクエストの完了、または、新しいリソースの識別のために、受信者を Request-URI 以外の場所にリダイレクトするのに使われます。

  .. method:: make_conditional(request_or_envrion)

     リクエストに対するレスポンスコンディショナルを生成します。このメソッドはレスポンス用の etag が既に定義されている場合に機能します。 ``add_etag`` メソッドを使って etag を追加できます。 etag なしで呼び出された場合、date ヘッダをセットするだけです。

     このメソッドは、リクエストか envrion 中のリクエストメソッドが ``GET`` か ``HEAD`` 以外の場合、何もしません。

     ``return resp.make_conditional(req)`` と書くと自分自身を返しますが、配置済みのオブジェクトは書き換えられます。

     :param request_or_environ: レスポンスコンディショナルを再度作成するのに使うリクエストオブジェクトか WSGI env。

   
  .. attribute:: mimetype

     ``content-type`` と似ていますが、パラメータ（例：文字セット、型など）がありません。例えばコンテントタイプが ``text/html; charset=utf-8`` の場合 mimetype は ``'text/html'`` となります。

  .. attribute:: mimetype_params

     mimetype パラメータがディクショナリで格納されています。例えば、コンテントタイプが ``text/html; charset=utf-8`` の場合、パラメータは ``{'charset': 'utf-8'}`` のようになっています。

  .. attribute:: response

     アプリケーションイテレータです。文字列で構成されていればリストになり、それ以外では、アプリケーションイテレータとして提供されます。

  .. attribute:: retry_after

     Retry-After レスポンスヘッダフィールドは、リクエストしているクライアントにサービスがどのくらいの時間利用できないかを示すために 503 (Service Unavailable) レスポンスとともに使われます。

  .. method:: set_cookie (key, value='', max_age=None, expires=None, path='/', domain=None, secure=None, httponly=False)

     cookie をセットします。パラメータは、Python スタンダードライブラリの cookie ``Morsel`` オブジェクトと同じですが、 unicode のデータも可です。

     :param key: セットされる cookie のキーです。
     :param value: cookie の値です。
     :param max_age: 秒数で指定します。cookie の保存期間がクライアントのブラウザセッションと同じでよければ ``None`` (デフォルト値) にします。
     :param domain: クロスドメインcookieをセットしたい場合に使います。例えば、 ``domain=".exmaple.com"`` だと、 "www.example.com" と "foo.example.com" ドメインから読み込める cookie がセットされます。指定がなければ、セットしたドメインからのみ読み込める cookie がセットされます。
     :param path: cookie のパスを制限します。デフォルトではドメイン全体です。
      
  .. method:: set_etag(etag, weak=False)

     etag をセットします。もし、古いのがあれば上書きします。
   
  .. attribute:: status

     文字列のステータスか、整数値のステータスコードを渡します。

  .. attribute:: status_code

     レスポンスステータスです。整数値です。

  .. attribute:: stream

     書き込み専用のレスポンスイテラブルです。

  .. attribute:: vary

     Vary フィールドは、レスポンスが新しいものである間、キャッシュがそのレスポンスをリヴァリデーションなしに後続のリクエストへの応答に使うことを許可されているか否かを完全に決定するリクエストヘッダフィールドの集合を示します。
   
  .. attribute:: www_authenticate

     パースされたフォームの ``www-authenticate`` ヘッダです。


生成方法
--------

レスポンスオブジェクトは、 ``werkzeug.Response`` クラスのインスタンスです。Kay には、レスポンスを生成するための関数が用意されています。
:func:`kay.utils.render_to_response`

HTTP エラー
-----------


:mod:``werkzeug.exceptions`` には沢山の例外が定義されています。これらのクラス名は HTTP エラーの種類を表しています。HTTP エラーを返したい場合は、これらの例外を raise してください。

HTTP エラーのリストです。

.. currentmodule:: werkzeug.exceptions

.. class:: HTTPException
.. class:: BadRequest
.. class:: Unauthorized
.. class:: Forbidden
.. class:: NotFound
.. class:: MethodNotAllowed
.. class:: NotAcceptable
.. class:: RequestTimeout
.. class:: Gone
.. class:: LengthRequired
.. class:: PreconditionFailed
.. class:: RequestEntityTooLarge
.. class:: RequestURITooLarge
.. class:: UnsupportedMediaType
.. class:: InternalServerError
.. class:: NotImplemented
.. class:: BadGateway
.. class:: ServiceUnavailable


.. seealso:: http://werkzeug.pocoo.org/documentation/dev/wrappers.html


