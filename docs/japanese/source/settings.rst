.. module:: settings

=======================
settings (設定ファイル)
=======================

Kayアプリケーションの基本的な設定はプロジェクトディレクトリ直下の ``settings.py`` で行います。デフォルト設定は ``kay/conf/global_settings.py`` に記載されています。


設定項目
--------


.. attribute:: APP_NAME

   アプリケーション名を設定します。デフォルト値は ``kay_main`` です。

   
.. attribute:: DEFAULT_TIMEZONE

   タイムゾーンを文字列で設定します。デフォルト値は ``Asia/Tokyo`` です。未設定の場合、Kayは自動的に ``UTC`` を設定します。有効なタイムゾーンの一覧は ``kay/lib/pytz/all_timezone`` を参照すれば得られます。

   
.. attribute:: DEBUG

   デバッグ機能の有効/無効を設定します。有効にする場合は ``True``, 無効にする場合は ``False`` を設定します。デフォルト値は ``True`` です。デバッグを有効にすると、Werkzeugのデバッガを使用することができます。サービスの実運用環境では ``False`` に設定してください。

   
.. attribute:: PROFILE

   プロファイリングの有効/無効を設定します。有効にすると、実行時のパフォーマンス測定結果がHTMLに出力されます。有効にする場合は ``True``, 無効にする場合は ``False`` を設定します。デフォルト値は ``False`` です。

   
.. attribute:: PRINNT_CALLERS_ON_PROFILING

   プロファイリング実施時の関数の呼び出し元出力のオン・オフを設定します。有効にする場合は ``True``, 無効にする場合は ``False`` を設定します。デフォルト値は ``False`` です。

   
.. attribute:: PRINNT_CALLEES_ON_PROFILING

   プロファイリング実施時の呼ばれた関数出力のオン・オフを設定します。有効にする場合は ``True``, 無効にする場合は ``False`` を設定します。デフォルト値は ``False`` です。

   
.. attribute:: SECRET_KEY

   ハッシュ値を生成するためのシードを設定します。デフォルト値は ``ReplaceItWithSecretString`` です。必ず書き換えるようにしてください。

   
.. attribute:: SESSION_PREFIX

   セッション名のプリフィックスを設定します。セッション機能で使用されます。デフォルト値は ``gaesess:`` です。

   
.. attribute:: COOKIE_AGE

   Cookieの有効期限(単位：秒)を設定します。デフォルト値は ``1209600`` (2週間)です。

   
.. attribute:: COOKIE_NAME

   Cookieの名前を設定します。デフォルト値は ``KAY_SESSION`` です。

   
.. attribute:: SESSION_MEMCACHE_AGE

   セッション情報の有効期限を設定します。デフォルト値は ``3600`` (1時間) です。

   
.. attribute:: LANG_COOKIE_AGE

   表示言語用のCookieの有効期限を設定します。デフォルト値は上述の ``COOKIE_AGE`` となっています。

   .. seealso:: :doc:`i18n`
   
.. attribute:: LANG_COOKIE_NAME

   表示言語のCookieの名称を設定します。デフォルト値は ``hl`` です。国際化が有効になっている場合、KayはこのCookieに設定されている言語でサイトを表示します。設定がない場合はブラウザの Accept-Language 設定から使用する言語を決定します。

   
.. attribute:: CACHE_MIDDLEWARE_SECONDS

   viewの関数が返したHTMLレスポンスのキャッシュの有効時間を設定（単位：秒）します。デフォルト値は ``3600`` （1時間）です。

   
.. attribute:: CACHE_MIDDLEWARE_NAMESPACE

   上記のキャッシュのネームペースを指定します。デフォルト値は ``CACHE_MIDDLEWARE`` です。

   
.. attribute:: CACHE_MIDDLEWARE_ANONYMOUS_ONLY

   上記のキャッシュをログインしていない時のみ適用するかどうかを設定します。デフォルト値は ``True`` です。

   
.. attribute:: ADD_APP_PREFIX_TO_KIND

   ``db.Model.kind()`` メソッドにアプリケーション名の prefix を付けるかどうかを設定します。有効にする場合は ``True``, 無効にする場合は ``False`` を設定します。デフォルト値は ``True`` です。有効にすると ``kind()`` の値は ``applicaion名_model名`` (全て小文字に変換される)となります。

.. attribute:: FORMS_USE_XHTML

   ``True`` にセットすると :mod:`kay.utils.forms` は xhtml としてフォームをレンダリングします。 デフォルト値は ``False`` です。

   
.. attribute:: ROOT_URL_MODULE

   Kayでは各アプリケーション配下の ``urls.py`` 以外に、URL設定ファイルをもつことができます。ここにはURLファイルのモジュール名を設定します。デフォルト値は ``urls`` です。

   
.. attribute:: MEDIA_URL

   メディアファイルのパスを指定します。デフォルト値は ``/media`` です。

   
.. attribute:: INTERNAL_MEDIA_URL

   ``kay.auth`` など bundle アプリが使用するメディアファイルを保存するパスを指定します。デフォルト値は ``/_media`` です。

   
.. attribute:: ADMINS

   管理者のユーザ名とメールアドレスをタプルで設定します。サーバー上で例外が発生した場合、ここで設定したメールアドレスにトレースバックが送信されます。デバッグ設定が無効（ ``DEBUG=False`` ）の場合のみ機能します。

   （設定例）

   .. code-block:: python

      ADMINS = (
        ('John', 'john@example.com'),
        ('Mary', 'mary@example.com')
      )

	  
.. attribute:: TEMPLATE_DIRS

   アプリケーションのテンプレートに対して、優先的に使用されるテンプレートファイルを保存するディレクトリをタプルで指定します。アプリケーションごとにもっているテンプレートを上書きしたい場合などに使用します。デフォルト値は空のタプルです。

   
.. attribute:: USE_I18N

   国際化の有効/無効を設定します。 ``True`` で有効、 ``False`` で無効になります。デフォルト値は ``True`` です。

   .. seealso:: :doc:`i18n`

   
.. attribute:: DEFAULT_LANG

   アプリケーションのデフォルト言語を指定します。デフォルト値は ``en`` です。kay がユーザーの使用する言語を特定できなかった時にこの値が使われます。

   
.. attribute:: INSTALLED_APPS

   このタプルには有効にしたいアプリケーション名を設定します。デフォルト値は空のタプルです。

   .. seealso:: :doc:`urlmapping`

   
.. attribute:: APP_MOUNT_POINTS

   この辞書にはそれぞれのアプリケーションにアクセスするためのURLパスを指定します。アプリケーションがキー、URLパスが値となります。未設定のアプリに対しては、 ``/アプリのモジュール名`` が自動的に設定されます。

   .. code-block:: python

     APP_MOUNT_POINTS = {
       'bbs': '/',
       'categories': '/c',
     }

   
.. attribute:: CONTEXT_PROCESSORS

   コンテキスト・プロセッサのパスをタプルで指定します。コンテキスト・プロセッサを使うとテンプレートエンジンが render の時に使用するコンテキストに追加設定できます。デフォルト値は空のタプルです。
   以下は設定の一例です。

   .. code-block:: python

      CONTEXT_PROCESSORS = (
        'kay.context_processors.request',
        'kay.context_processors.url_functions',
        'kay.context_processors.media_url',
      )
  

.. attribute:: JINJA2_FILTERS

   Jinja2のフィルタをディクショナリで設定します。デフォルト値は空の辞書です。
   以下は設定例です。

   .. code-block:: python

      JINJA2_FILTERS = {
        'nl2br': 'kay.utils.filters.nl2br',
      }

	  
.. attribute:: JINJA2_ENVIRONMENT_KWARGS

   Jinja2のコンストラクタに渡すキーワード引数を指定できます。デフォルト値は以下のとおりです。

   .. code-block:: python

      JINJA2_ENVIRONMENT_KWARGS = {
        'autoescape': True,
      }

	
.. attribute:: JINJA2_EXTENSIONS

   Jinja2のエクステンションを追加する際に、このタプルに設定します。デフォルト値は以下のとおりです。

   .. code-block:: python

      JINJA2_EXTENSIONS = (
        'jinja2.ext.i18n',
      )

	  
.. attribute:: SUBMOUNT_APPS

   全く別の settings にて起動させたいアプリケーションをここに設定します。デフォルト値は空のタプルです。

   
.. attribute:: MIDDLEWARE_CLASSES

   ミドルウェアを追加する場合は、このタプルに設定します。デフォルト値は空のタプルです。以下は設定の一例です。

   .. code-block:: python

     MIDDLEWARE_CLASSES = (
       'kay.session.middleware.SessionMiddleware',
       'kay.auth.middleware.AuthenticationMiddleware',
     )

	  
.. attribute:: AUTH_USER_BACKEND

   ユーザ認証で使用するバックエンドクラスを指定します。デフォルト値は ``kay.auth.backends.googleaccount.GoogleBackend`` です。

   .. seealso:: :doc:`auth`

   
.. attribute:: AUTH_USER_MODEL

   バックエンドで認証されたユーザデータを保存するクラスを指定します。 ``GoogleUser`` を継承したユーザクラスを認証に使う場合などはここに設定する必要があります。デフォルト値は ``kay.auth.models.GoogleUser`` です。

   .. seealso:: :doc:`auth`

   
.. attribute:: USE_DB_HOOK

   DBフックの有効/無効を設定します。Djangoのシグナルに相当します。DBに対して何らかのアクションがあった場合に起動させる処理がある場合は ``True`` を設定します。DBフックについてあまり詳しくない場合は ``False`` を指定してください。

