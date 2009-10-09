.. module:: settings

============
設定ファイル
============

Kayアプリケーションの基本的な設定は ``settings.py`` で行います。元ファイルは ``kay/kay/conf/global_settings.py`` です。


設定項目
--------

.. attribute:: APP_NAME

   アプリケーション名を設定します。デフォルト値は ``kay_main`` です。???

.. attribute:: DEFAULT_TIMEZONE

   タイムゾーンを文字列で設定します。デフォルト値は ``Asia/Tokyo`` です。未設定の場合、Kayは自動的に ``UTC`` を設定します。

.. attribute:: DEBUG

   デバッグ機能の有効/無効を設定します。有効にする場合は ``True``, 無効にする場合は ``False`` を設定します。デフォルト値は ``True`` です。デバッグを有効にすると、Werkzeugのデバッガを使用することができます。運用環境では ``False`` に設定してください。

.. attribute:: PROFILE

   プロファイリングの有効/無効を設定します。有効にすると、実行時のパフォーマンス測定結果がHTMLに出力されます。有効にする場合は ``True``, 無効にする場合は ``False`` を設定します。デフォルト値は ``False`` です。

.. attribute:: PRINNT_CALLERS_ON_PROFILING

   プロファイリング実施時の関数の呼び出し元出力のオン・オフを設定します。有効にする場合は ``True``, 無効にする場合は ``False`` を設定します。デフォルト値は ``False`` です。

.. attribute:: PRINNT_CALLEES_ON_PROFILING

   プロファイリング実施時の呼ばれた関数出力のオン・オフを設定します。有効にする場合は ``True``, 無効にする場合は ``False`` を設定します。デフォルト値は ``False`` です。

.. attribute:: SECRET_KEY

   ハッシュ値を生成するためのシードを設定します。デフォルト値は ``hogehoge`` です。

.. attribute:: SESSION_PREFIX

   セッション名のプリフィックスを設定します。セッション機能で使用されます。デフォルト値は ``gaesess:`` です。

.. attribute:: COOKIE_AGE

   Cookieの有効期限(単位：秒)を設定します。デフォルト値は ``1209600`` (2週間)です。

.. attribute:: COOKIE_NAME

   Cookieの名前を設定します。デフォルト値は ``KAY_SESSION`` です。

.. attribute:: SESSION_MEMCACHE_AGE

   セッション情報の有効期限を設定します。デフォルト値は ``3600`` (1時間) です。

.. attribute:: LANG_COOKIE_AGE

   表示言語用のCookieの有効期限を設定します。国際化が有効になっている場合、KayはこのCookieに設定されている言語でサイトを表示します。設定がない場合はブラウザの言語設定を参照します。Cookieはサイトの言語選択のリンクをクリックしたときに保存されます。デフォルト値は上述の ``COOKIE_AGE`` となっています。

.. attribute:: LANG_COOKIE_NAME

   上記の表示言語のCookieの名称を設定します。デフォルト値は ``hl`` です。

.. attribute:: CACHE_MIDDLEWARE_SECONDS

   viewの関数が返したHTMLレスポンスのキャッシュの有効時間を設定（単位：秒）します。デフォルト値は ``3600`` （1時間）です。

.. attribute:: CACHE_MIDDLEWARE_NAMESPACE

   上記のキャッシュのネームペースを指定します。デフォルト値は ``CACHE_MIDDLEWARE`` です。

.. attribute:: CACHE_MIDDLEWARE_ANONYMOUS_ONLY

   上記のキャッシュをログインしていない時のみ適用するかどうかを設定します。デフォルト値は ``True`` です。
   
.. attribute:: ADD_APP_PREFIX_TO_KIND

   データストアのprefixを設定します。デフォルト値は ``applicaion名_model名`` となります。

.. attribute:: ROOT_URL_MODULE

   Kayでは各アプリケーション配下の ``urls.py`` 以外に、URL設定ファイルをもつことができます。ここにはURLファイルのパスを設定します。デフォルト値は ``urls`` です。

.. attribute:: MEDIA_URL

   アプリケーションごとにメディアファイルをもたせる際のパスを指定します。デフォルト値は ``media`` です。各アプリケーションの配下にここで指定したパスのディレクトリを作成します。

.. attribute:: INTERNAL_MEDIA_URL

   kay.authなどのミドルウェアが使用するメディアファイルを保存するパスを指定します。デフォルト値は ``media`` です。

.. attribute:: ADMINS

   管理者のメールアドレスを設定します。サーバエラーが発生した場合、ここで設定したメールアドレスにトレースバックが送信されます。デバッグ設定が無効（ ``DEBUG=False`` ）の場合のみ機能します。
   
.. attribute:: TEMPLATE_DIRS

   アプリケーションのテンプレートに対して、優先的に使用されるテンプレートファイルを保存するディレクトリを指定します。アプリケーション毎にもっているテンプレートを上書きしたい場合などに使用します。デフォルト値は ``templates`` です。

.. attribute:: USE_I18N

   国際化の有効/無効を設定します。 ``True`` で有効、 ``False`` で無効になります。デフォルト値は ``False`` です。

.. attribute:: DEFAULT_LANG

   アプリケーションのデフォルト言語を指定します。デフォルト値は ``en`` です。

.. attribute:: INSTALLED_APPS

   このタプルには有効にしたいアプリケーション名を設定します。デフォルト値は空のタプルです。

.. attribute:: APP_MOUNT_POINTS

   このタプルにはアプリケーションにアクセスするためのURLパスを指定します。未設定の場合、 ``/各アプリケーション名`` が設定されます。

.. attribute:: CONTEXT_PROCESSORS

   コンテキスト・プロセッサのパスを指定します。テンプレートエンジンで、変数と値のマッピング（コンテキスト）を指定したファイルのパスをタプルで設定します。デフォルト値は、 ``'kay.context_processors.request', 'kay.context_processors.url_functions', 'kay.context_processors.media_url',`` です。


.. attribute:: JINJA2_FILTERS

   Jinja2の :keyword:`filter` をディクショナリで設定します。デフォルト値は ``'nl2br': 'kay.utils.filters.nl2br'`` です。

.. attribute:: JINJA2_ENVIRONMENT_KWARGS

   Jinja2の ``'autoescape': True`` 

.. attribute:: JINJA2_EXTENSIONS

   Jinja2のエクステンションを追加する際に設定します。

.. attribute:: SUBMOUNT_APPS

   Kayに付属するミドルウェアを一切使わずに起動させたいアプリケーションがある場合は、ここに設定します。この機能は将来的に削除する可能性があります。

.. attribute:: MIDDLEWARE_CLASSES

   

.. attribute:: AUTH_USER_BACKEND

   ユーザ認証で使用するバックエンドクラスを指定します。デフォルトは ``kay.auth.backend.DatastoreBackend`` です。

.. attribute:: AUTH_USER_MODEL

   バックエンドで認証されたユーザデータを保存するクラスを指定します。 ``GoogleUser`` を継承したユーザクラスを認証に使う場合などは、ここに設定する必要があります。デフォルト値は ``kay.auth.models.GoogleUser`` です。
   

.. attribute:: USE_DB_HOOK

   DBフックの有効/無効を設定します。Djangoのシグナルに相当します。DBに対して何らかのアクションがあった場合に起動させる処理がある場合は、 ``True`` を設定します。扱いが困難なため、通常は ``False`` を指定してください。



