==========
認証の設定
==========

概要
----

Google App Engine には、良くできた認証機構が備わっています。この機構では Google Account か Google Apps Account をバックエンドとして利用します。
Kay では ``AuthenticationMiddleware`` と ``kay.auth.backends.googleaccount.GoogleBackend`` を使用する事でこの機能を拡張可能な形で利用する事ができます。また、データストアに保存したユーザー名とパスワードを認証に使用する事もできます。

認証用ミドルウェアを有効にする
------------------------------

Kay の認証機構を使用するには、 :attr:`settings.MIDDLEWARE_CLASSES` に ``kay.auth.middleware.AuthenticationMiddleware`` を追加する必要があります。

Google Account 認証を使用する
-----------------------------

:attr:`settings.AUTH_USER_BACKEND` のデフォルト値は ``kay.auth.backends.googleaccount.GoogleBackend`` です。この設定は、Google Account か Google Apps Account を使用して認証するためのものです。ユーザーが初めてアプリケーションにログインした時、そのユーザーの情報が ``GoogleUser`` (デフォルトの設定です。これもカスタマイズ可能です)エンティティとしてデータストアに保存されます。この backend の使用には、セッション機能を必要としません。

ユーザーモデルを変更するには ``kay.auth.models.GoogleUser`` を継承して必要なプロパティを追加したモデルを定義し、そのモデルのクラス名を ``AUTH_USER_MODEL`` に設定する必要があります。

.. code-block:: python

  MIDDLEWARE_CLASSES = (
    'kay.auth.middleware.AuthenticationMiddleware',
  )
  AUTH_USER_BACKEND = 'kay.auth.backends.googleaccount.GoogleBackend'
  AUTH_USER_MODEL = 'kay.auth.models.GoogleUser'


データストアを利用した認証
--------------------------

このタイプの認証を使用するには :attr:`settings.AUTH_USER_MODEL` に ``kay.auth.models.DatastoreUser`` (又はそれを継承したクラス) を、加えて :attr:`settigns.AUTH_USER_BACKEND` に ``kay.auth.backends.datastore.DatastoreBackend`` を設定する必要があります。
``AuthenticationMiddleware`` はこのミドルウェアの動作に必要な ``SessionMiddleware`` の下に設定する必要があります。
また ``kay.auth`` を :attr:`settings.INSTALLED_APPS` に登録する必要もあります。

.. code-block:: python

  INSTALLED_APPS = (
    'kay.auth',
  )
  MIDDLEWARE_CLASSES = (
    'kay.sessions.middleware.SessionMiddleware',
    'kay.auth.middleware.AuthenticationMiddleware',
  )
  AUTH_USER_BACKEND = 'kay.auth.backends.datastore.DatastoreBackend'
  AUTH_USER_MODEL = 'kay.auth.models.DatastoreUser'


ヘルパ関数とデコレーター
------------------------

``kay.utils`` モジュールには二つのヘルパ関数があります:
``create_logout_url`` と ``create_login_url`` です。これらの関数はテンプレートをレンダリング際のコンテキストに自動的にインポートされます。従ってテンプレート内部では、下記のように使用する事ができます:

.. code-block:: html

  {% if request.user.is_anonymous() %}
    <a href="{{ create_login_url() }}">login</a>
  {% else %}
    Hello {{ request.user }}! <a href="{{ create_logout_url() }}">logout</a>
  {% endif %}

``kay.auth.decorators`` モジュールには、二つのデコレーターがあります:
``login_required`` と ``admin_required`` です。これらのデコレーターでビューを修飾するには下記のようにします:

.. code-block:: python

  @login_required
  def user_profile(request):
    """ This is a view for detailed information of the user's profile. 
    """
    ...
    ...
    
  @admin_required
  def manage_users(request):
    """ This is a view for user management.
    """
    ...
    ...

ユーザーの作成
--------------

``kay.auth.create_new_user`` はユーザー作成用の関数です。既に同じユーザー名が登録されていると ``kay.auth.DuplicateKeyError`` 例外が raise されます。成功すると新しく作成されたユーザーオブジェクトが返ります。

.. code-block:: python

   from kay.auth import create_new_user
   user_name = 'hoge'
   password = 'hoge'
   new_user = create_new_user(user_name, password, is_admin=is_admin)

次のように ``manage.py create_user`` を使う事もできます:

.. code-block:: bash

   $ python manage.py create_user hoge

このコマンドは、新しいユーザーのパスワードを尋ねてきます。

ログインボックスの表示
----------------------

ログインボックスを使用するには、 :attr:`settings.CONTEXT_PROCESSORS` に
``kay.auth.context_processors.login_box`` を追加し、テンプレートでは
``auth/macros.html`` からインポートした ``render_loginbox`` マクロを好
きな場所で使用します。下記は使用例です:

settings.py:

.. code-block:: python

   CONTEXT_PROCESSORS = (
     'kay.context_processors.request',
     'kay.context_processors.url_functions',
     'kay.context_processors.media_url',
     'kay.auth.context_processors.login_box'
   )

template:

.. code-block:: html

   {% from "auth/macros.html" import render_loginbox with context %}

   {% if request.user.is_anonymous() %}
     {{ render_loginbox() }}
   {% else %}
     Hello {{ request.user }}! <a href="{{ create_logout_url() }}">logout</a>
   {% endif %}

独自ドメイン上でデータストア認証を使用する
------------------------------------------

TODO