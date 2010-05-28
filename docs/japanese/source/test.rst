===========
Test の実施
===========

概要
----

:option:`manage.py test -t` 又はオプション無しの ``manage.py test`` を使用してアプリケーションのテストができます。 ``kay.ext.testutils.gae_test_base.GAETestBase`` を拡張してテストを書く事を強くお勧めします。なぜなら ``GAETestBase`` は設定に応じてテスト用の環境を整えてくれるからです。 ``GAETestBase`` の動作を変更するには、テストケースにクラス属性を定義する事で行います。

テストの実行は下記のいずれかの方法で行います::

  * ``python manage.py test`` とタイプして test サブコマンドを実行する
  * 開発サーバーや appspot の ``/_ah/test`` にアクセスする。

.. Note::

   本番環境でテストを実行する場合には、全てのテストが並列で実行されます。
   これによって予期せぬ動作をするかもしれません。本番環境でもテストをす
   る場合は、他のテストに影響を与えないように書きましょう。

初めてのテスト
--------------

Kay のテストコマンドでは、APP_DIR 以下の tests モジュール(又はパッケージ)から TestCase を自動で見付けて実行してくれます。ここでは myapp/tests/__init__.py にテストを書くことにします。

myapp/tests/__init__.py:

.. code-block:: python

  from google.appengine.ext import db

  from kay.ext.testutils.gae_test_base import GAETestBase

  from myapp.models import Comment

  class ModelTest(GAETestBase):
    def tearDown(self):
      db.delete(Comment.all().fetch(10))

    def test_model(self):
      c = Comment(body=u'Hello Test!')
      c.put()
      comments = Comment.all().fetch(100)
      self.assertEquals(len(comments), 1)
      self.assertEquals(comments[0].body, 'Hello Test!')

このテストでは myapp.models.Comment についてテストしています。Datastore などの stub は自動でセットアップされているので簡単にテストが書けますね。

各種設定
------------

``GAETestBase`` の動作は前述したようにクラス属性を設定することにより行
います。 ``KIND_PREFIX_IN_TEST`` のデフォルト値は ``'t'`` ですが、それ
以外の属性のデフォルト値は ``False`` です。


* USE_PRODUCTION_STUBS

  この属性が ``True`` だと、本番サーバーにてテストを実行した時に
  ``GAETestBase`` は本番環境のデータストアを使用してテストを行います。

* USE_REMOTE_STUBS

  この属性が ``True`` だと ``manage.py`` を使用してテストを実行した時に
  ``GAETestBase`` は remote_api を経由し、本番環境のデータストアを使用
  してテストを行います。

* CLEANUP_USED_KIND

  この属性が ``True`` だと ``GAETestBase`` はテスト内でアクセスしたエン
  ティティを全て消去します。

* KIND_NAME_UNSWAPPED

  この属性が ``True`` だと ``GAETestBase`` はプレフィックス付きの kind
  では無く、オリジナルの kind を使用します。

* KIND_PREFIX_IN_TEST

  デフォルトでは ``GAETestBase`` は全てのモデルの kind に ``t_`` という
  プレフィックスを付けます。この属性によりこのプレフィックスを変更でき
  ます。属性値を ``test`` とすればプレフィックスとして ``test_`` が使用
  されます。

例えば、 ``CLEANUP_USED_KIND`` を ``True`` にすれば、 ``GAETestBase``
がエンティティの後始末をしてくれるので、最初に挙げたテストの
``tearDown()`` メソッドは必要無くなります。

他の例としては、 ``USE_PRODUCTION_STUBS`` を ``True`` にすれば本番環境
でのテストを行う事ができます。

myapp/tests/__init__.py:

.. code-block:: python

  from google.appengine.ext import db

  from kay.ext.testutils.gae_test_base import GAETestBase

  from myapp.models import Comment

  class ModelTest(GAETestBase):

    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def test_model(self):
      c = Comment(body=u'Hello Test!')
      c.put()
      comment = Comment.get(c.key())
      self.assertEquals(comment.body, 'Hello Test!')


テスト用 Client を使用する
--------------------------

今度は Web アプリとしての動きをテストしてみましょう。それには werkzeug の Client というクラスと ``kay.utils.test`` モジュールを使用すると良いでしょう。


myapp/tests/__init__.py:

.. code-block:: python

  from google.appengine.ext import db
  from werkzeug import BaseResponse, Client, Request
  from kay.app import get_application
  from kay.utils.test import (
    init_recording, get_last_context, get_last_template, disable_recording
  )
  from kay.ext.testutils.gae_test_base import GAETestBase

  from myapp.models import Comment

  class MyappTestCase(unittest.TestCase):
    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def setUp(self):
      init_recording()
      app = get_application()
      self.client = Client(app, BaseResponse)

    def tearDown(self):
      disable_recording()

    def test_post(self):
      response = self.client.get('/')
      self.assertEquals(response.status_code, 200)
      used_template = get_last_template()
      used_context = get_last_context()
      csrf_token = used_context['form'].csrf_token
      response = self.client.post('/', data={'comment': 'Hello',
					     '_csrf_token': csrf_token},
				  follow_redirects=True)
      comments = Comment.all().fetch(100)
      self.assertEquals(len(comments), 1)

``werkzeug.Client`` クラスを使用すればアプリケーションの動きをテストできます。また ``init_recording`` を実行した後ならば ``get_last_template`` と ``get_last_context`` 関数で最後に使用した template の名前や context を知る事ができます。

.. seealso:: `Werkzeug test utitilies <http://werkzeug.pocoo.org/documentation/0.5.1/test.html>`_

これらのテストを実行すると下記のように出力されます。ここでは -v2 でテスト名も表示しています。

.. code-block:: bash

  $ python manage.py test -v2
  Running on Kay-0.3.0
  test_model (myapp.tests.ModelTest) ... ok
  test_post (myapp.tests.MyappTestCase) ... ok

  ----------------------------------------------------------------------
  Ran 2 tests in 0.093s

  OK

ログの出力先を指定する
----------------------

アプリケーションのログを見るためには、下記のように logging の設定を行います。

.. code-block:: python

  import logging
  logging.basicConfig(filename="test-debug.log", level=logging.DEBUG)

同じような行を個別の setUp メソッド内に書くこともできます:

.. code-block:: python

  import logging

  from google.appengine.ext import db

  from werkzeug import BaseResponse, Client, Request
  from kay.app import get_application
  from kay.ext.testutils.gae_test_base import GAETestBase

  from myapp.models import Comment

  class MyappTestCase(unittest.TestCase):
    def setUp(self):
      logging.basicConfig(filename="test-debug.log", level=logging.DEBUG)
      app = get_application()
      self.client = Client(app, BaseResponse)
    # ..
    # ..
