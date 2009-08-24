==========
認証の設定
==========

概要
----

Google App Engine には、良くできた認証機構が備わっています。この機構では Google Account か Google Apps Account をバックエンドとして利用します。
Kay では ``GoogleAuthenticationMiddleware`` を使用する事でこの機能を拡張可能な形で利用する事ができます。また、データストアに保存したユーザー名とパスワードを認証に使用する事もできます。

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

Google Account 認証を使用する
-----------------------------

``kay.auth.middleware.GoogleAuthenticationMiddleware`` がデフォルトで有効になっています。このミドルウェアは、Google Account か Google Apps Account を使用して認証するためのものです。ユーザーが初めてアプリケーションにログインした時、そのユーザーの情報が ``GoogleUser`` (デフォルトの設定です。これもカスタマイズ可能です)エンティティとしてデータストアに保存されます。このミドルウェアの使用には、セッション機能を必要としません。

ユーザーモデルを変更するには、``kay.auth.models.GoogleUser`` を継承して必要なプロパティを追加したモデルを定義し、そのモデルのクラス名を ``AUTH_USER_MODEL`` に設定する必要があります。

.. code-block:: python

  MIDDLEWARE_CLASSES = (
    'kay.auth.middleware.GoogleAuthenticationMiddleware',
  )
  AUTH_USER_MODEL = 'kay.auth.models.GoogleUser'


データストアを利用した認証
--------------------------

このタイプの認証を使用するには ``kay.auth.middleware.AuthenticationMiddleware`` を ``MIDDLEWARE_CLASSES`` に設定し、また ``AUTH_USER_MODEL`` には ``kay.auth.models.DatastoreUser`` (又はそれを継承したクラス) を設定する必要があります。
``AuthenticationMiddleware`` はこのミドルウェアの動作に必要な ``SessionMiddleware`` の下に設定する必要があります。

.. code-block:: python

  MIDDLEWARE_CLASSES = (
    'kay.sessions.middleware.SessionMiddleware',
    'kay.auth.middleware.AuthenticationMiddleware',
  )
  AUTH_USER_MODEL = 'kay.auth.models.DatastoreUser'

現在では、データストアにユーザーを作成する便利な手段は存在しません。ユーザーのパスワードを保存する場合には、特別なハッシュフォーマットで保存する必要がありますので気をつけてください。それには ``kay.utils.crypto.gen_pwhash`` 関数が使用できます。パフォーマンスのため、key_name を指定する必要もあります。下記に新しいユーザーを作成するコードを示します:

.. code-block:: python

   from kay.utils.crypto import gen_pwhash
   from kay.auth.models import DatastoreUser

   user_name = 'newuser'
   password = 'newpassword'

   new_user = DatastoreUser(key_name=DatastoreUser.get_key_name(user_name),
                            user_name=user_name, password=gen_pwhash(password))
   new_user.put()

独自ドメイン上でデータストア認証を使用する
------------------------------------------

TODO