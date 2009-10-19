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

今度は Web アプリとしての動きをテストしてみましょう。それには werkzeug の Client というクラスを使用すると良いでしょう。


myapp/tests/__init__.py:

.. code-block:: python

  import unittest

  from werkzeug import BaseResponse, Client, Request
  from kay.app import get_application
  from google.appengine.ext import db

  from myapp.models import Comment

  class MyappTestCase(unittest.TestCase):
    def setUp(self):
      app = get_application()
      self.client = Client(app, BaseResponse)

    def tearDown(self):
      db.delete(Comment.all().fetch(10))

    def test_post(self):
      response = self.client.get('/')
      import re
      m = re.search(r'name="_csrf_token" value="([^"]+)"', response.data)
      response = self.client.post('/', data={'comment': 'Hello',
					     '_csrf_token': m.group(1)},
				  follow_redirects=True)
      comments = Comment.all().fetch(100)
      self.assertEquals(len(comments), 1)

``werkzeug.Client`` クラスを使用すればアプリケーションの動きをテストできます。現在のところ、Response の解析は手動で(上記の例では re モジュールを使用しています)行うことになります。

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