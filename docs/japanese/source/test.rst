===========
Test の実施
===========

概要
----

:option:`manage.py test -t` 又はオプション無しの ``manage.py test`` を使用してアプリケーションのテストができます。 ``manage.py`` がテスト用に環境を整えてくれるので、手軽にテストが書けるようになっています。また werkzeug のテスト用ライブラリもご紹介します。

初めてのテスト
--------------

Kay のテストコマンドでは、APP_DIR 以下の tests モジュール(又はパッケージ)から TestCase を自動で見付けて実行してくれます。ここでは myapp/tests/__init__.py にテストを書くことにします。

myapp/tests/__init__.py:

.. code-block:: python

  import unittest

  from google.appengine.ext import db

  from myapp.models import Comment

  class ModelTest(unittest.TestCase):
    def tearDown(self):
      db.delete(Comment.all().fetch(10))

    def test_model(self):
      c = Comment(body=u'Hello Test!')
      c.put()
      comments = Comment.all().fetch(100)
      self.assertEquals(len(comments), 1)
      self.assertEquals(comments[0].body, 'Hello Test!')

このテストでは myapp.models.Comment についてテストしています。Datastore などの stub は自動でセットアップされているので簡単にテストが書けますね。


テスト用 Client を使用する
--------------------------

今度は Web アプリとしての動きをテストしてみましょう。それには werkzeug の Client というクラスと ``kay.utils.test`` モジュールを使用すると良いでしょう。


myapp/tests/__init__.py:

.. code-block:: python

  import unittest

  from google.appengine.ext import db
  from werkzeug import BaseResponse, Client, Request
  from kay.app import get_application
  from kay.utils.test import (
    enable_recording, get_last_context, get_last_template
  )

  from myapp.models import Comment

  class MyappTestCase(unittest.TestCase):
    def setUp(self):
      enable_recording()
      app = get_application()
      self.client = Client(app, BaseResponse)

    def tearDown(self):
      db.delete(Comment.all().fetch(10))

    def test_post(self):
      response = self.client.get('/')
      used_template = get_last_template()
      used_context = get_last_context()
      csrf_token = used_context['form'].csrf_token
      response = self.client.post('/', data={'comment': 'Hello',
					     '_csrf_token': csrf_token},
				  follow_redirects=True)
      comments = Comment.all().fetch(100)
      self.assertEquals(len(comments), 1)

``werkzeug.Client`` クラスを使用すればアプリケーションの動きをテストできます。また ``enable_recording`` を実行した後ならば ``get_last_template`` と ``get_last_context`` 関数で最後に使用した template の名前や context を知る事ができます。

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
  import unittest

  from werkzeug import BaseResponse, Client, Request
  from kay.app import get_application
  from google.appengine.ext import db

  from myapp.models import Comment

  class MyappTestCase(unittest.TestCase):
    def setUp(self):
      logging.basicConfig(filename="test-debug.log", level=logging.DEBUG)
      app = get_application()
      self.client = Client(app, BaseResponse)
    # ..
    # ..
