====================
セッションを使用する
====================

概要
----

Kay には匿名セッションの仕組があります。この仕組を有効にすると全ての ``request`` オブジェクトには自動的に ``session`` 属性が付加されます。pickle できるデータならなんでもこのセッションに格納できます。

設定
----

セッションを使用するには ``settings.py`` にて ``kay.sessions`` アプリケーション を ``INSTALLED_APPS`` へ ``kay.sessions.middleware.SessionMiddleware`` を ``MIDDLEWARE_CLASSES`` にセットする必要があります。

.. code-block:: python

  INSTALLED_APPS = (
    'kay.sessions',
    'myapp',
  )

  # ...

  MIDDLEWARE_CLASSES = (
    'kay.sessions.middleware.SessionMiddleware',
    'kay.auth.middleware.GoogleAuthenticationMiddleware',
  )

デコレーター
------------

``kay.sessions.decorators.no_session`` デコレーターを使用すれば、特定のビューではセッションを使用しないようにできます。下記のように使用します:

.. code-block:: python

  from kay.sessions.decorators import no_session

  def custom_page(request):
    """ This view use session capability.
    """
    #...
    #...

  @no_session
  def public_page(request):
    """ This view doesn't use session
    """
    #...
    #...


古いセッションを破棄する
------------------------

古いセッションを破棄するためのビューが ``kay.sessions.views.purge_old_sessions`` にあります。このビューはデフォルトでは ``/sessions/purge_old_sessions`` に結び付けられています。古いセッションを消したければ、このビューを cron か何かで定期的に呼出す必要があります。下記はサンプルの cron 設定です:

cron.yaml

.. code-block:: yaml

  cron:
  - description: purge old session data
    url: /sessions/purge_old_sessions
    schedule: every 1 hours


セッションにデータを保存する
----------------------------

``request.session`` を辞書のように扱ってください。下記は単純なカウンターの例です:

.. code-block:: python

  def index(request):
    count = request.session.get('count', 0) + 1
    request.session['count'] = count
    #...
    #...

