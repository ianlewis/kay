.. module:: settings

====================
Settings Config File
====================

This is a list of available settings that can be modified
to customize the behavior of your application.


Items
=====

.. attribute:: APP_NAME

   Specify the application name. Default value is ``kay_main``.

   
.. attribute:: DEFAULT_TIMEZONE

   Specify the default local timezone in string, e.g: 'Asia/Tokyo' The default is ``Asia/Tokyo``. If it's not specified Kay automatically set ``UTC``. You can get the valid TimeZone list by reffering ``kay/lib/pytz/all_timezone``.


.. attribute:: DEBUG

   This attribute has different effect on local dev server and
   appengine server.

   * Local environment:

     If DEBUG is set to True, werkzeug's debugger will come up on any
     uncaught exception. Otherwise, it just displays 500 error, and
     tracebacks will be printed on console.

   * Server environment:

     If DEBUG is set to True, it displays tracebacks on your browser
     on any uncaught exception. Otherwise, it displays a simple error
     message to end users, and tracebacks will be sent to
     administrators by email.


.. attribute:: PROFILE

   If set to ``True``, a profiling information will be displayed on the
   browser following normal application's response. The default is ``False``.


.. attribute:: PRINNT_CALLERS_ON_PROFILING

   If set to ``True``, callers will displayed on the browser with profiling information. The default is ``False``. 

   
.. attribute:: PRINNT_CALLEES_ON_PROFILING

   If set to ``True``, callees will displayed on the browser with profiling information. The default is ``False``. 

   
.. attribute:: SECRET_KEY

   Specify the seed to create hash value. The default is ``ReplaceItWithSecretString``. Please be sure to rewrite it.


.. attribute:: SESSION_PREFIX

   Specify the prefix of session name. The default is ``gaesess:``.

   
.. attribute:: COOKIE_AGE

   Specify the cookie age. The defautl is ``1209600`` (2 weeks).

   
.. attribute:: COOKIE_NAME

   Specify the cookie name. The default is ``KAY_SESSION``.

   
.. attribute:: SESSION_MEMCACHE_AGE

   Specify the session information age. The default is ``3600`` (1 hour).

   
.. attribute:: LANG_COOKIE_NAME

   Specify the name of the cookie for the language. The default is ``hl``.
   If i18n is enabled Kay will display pages in the language specified with this cookie,
   otherwise identify the language from Accept-Language setting of the browser.

   
.. attribute:: CACHE_MIDDLEWARE_SECONDS

   viewの関数が返したHTMLレスポンスのキャッシュの有効時間を設定（単位：秒）します。デフォルト値は ``3600`` （1時間）です。

   
.. attribute:: CACHE_MIDDLEWARE_NAMESPACE

   上記のキャッシュのネームペースを指定します。デフォルト値は ``CACHE_MIDDLEWARE`` です。

   
.. attribute:: CACHE_MIDDLEWARE_ANONYMOUS_ONLY

   上記のキャッシュをログインしていない時のみ適用するかどうかを設定します。デフォルト値は ``True`` です。

   
.. attribute:: ADD_APP_PREFIX_TO_KIND

   ``db.Model.kind()`` メソッドにアプリケーション名の prefix を付けるかどうかを設定します。有効にする場合は ``True``, 無効にする場合は ``False`` を設定します。デフォルト値は ``True`` です。有効にすると ``kind()`` の値は ``applicaion名_model名`` (全て小文字に変換される)となります。

   
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

   Allows you to specify the directory where Kay will look for your
   templates. This is a list of relative paths from your project root
   to your template directories.


.. attribute:: USE_I18N

   国際化の有効/無効を設定します。 ``True`` で有効、 ``False`` で無効になります。デフォルト値は ``True`` です。

   .. seealso:: :doc:`i18n`

   
.. attribute:: INSTALLED_APPS

   This tupple must contain application names you want to
   activate. Default value is an empty tupple.


.. attribute:: APP_MOUNT_POINTS

   この辞書にはそれぞれのアプリケーションにアクセスするためのURLパスを指定します。アプリケーションがキー、URLパスが値となります。未設定のアプリに対しては、 ``/アプリのモジュール名`` が自動的に設定されます。

   .. code-block:: python

     APP_MOUNT_POINTS = {
       'bbs': '/',
       'categories': '/c',
     }

   
.. attribute:: CONTEXT_PROCESSORS

   Specify the path of context processors in this tuple.
   If you add context proccssors,
   you can add contexts template engine use in rendering. The default as follows.

   .. code-block:: python

      CONTEXT_PROCESSORS = (
        'kay.context_processors.request',
        'kay.context_processors.url_functions',
        'kay.context_processors.media_url',
      )
  

.. attribute:: JINJA2_FILTERS

    A dictionary of filter name to callable filters that are automatically
    loaded into the Jinja2 environment.

	  
.. attribute:: JINJA2_ENVIRONMENT_KWARGS

   Jinja2のコンストラクタに渡すキーワード引数を指定できます。デフォルト値は以下のとおりです。

   .. code-block:: python

      JINJA2_ENVIRONMENT_KWARGS = {
        'autoescape': True,
      }

	
.. attribute:: JINJA2_EXTENSIONS

   A list of Jinja2 extension classes. These are automatically
   imported and loaded into the Jinja2 environment.


 .. attribute:: SUBMOUNT_APPS

   If you'd like to run applications with entirely-differnt settings, you can set them here. The default is an empty tuple.
   
.. attribute:: MIDDLEWARE_CLASSES

   Specify additional middlewares to this tuple.

   .. code-block:: python

     MIDDLEWARE_CLASSES = (
       'kay.auth.middleware.AuthenticationMiddleware',
     )

	  
.. attribute:: AUTH_USER_BACKEND

   ユーザ認証で使用するバックエンドクラスを指定します。デフォルト値は ``kay.auth.backend.GoogleBackend`` です。

   .. seealso:: :doc:`auth`

   
.. attribute:: AUTH_USER_MODEL

   バックエンドで認証されたユーザデータを保存するクラスを指定します。 ``GoogleUser`` を継承したユーザクラスを認証に使う場合などはここに設定する必要があります。デフォルト値は ``kay.auth.models.GoogleUser`` です。

   .. seealso:: :doc:`auth`

   
.. attribute:: USE_DB_HOOK

   DBフックの有効/無効を設定します。Djangoのシグナルに相当します。DBに対して何らかのアクションがあった場合に起動させる処理がある場合は ``True`` を設定します。DBフックについてあまり詳しくない場合は ``False`` を指定してください。


