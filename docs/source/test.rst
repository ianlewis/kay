=============
Running Tests
=============

Overview
--------

You can test your applications by invoking :option:`manage.py test --target`
or ``manage.py test`` without any options. ``manage.py`` script sets
up an environment for testing, so you can write your test code
easily. We will take a quick look on werkzeug's library for testing.


Your first test
---------------

``manage.py test`` automatically collects subclasses of TestCase from
tests module under your APP_DIR. So let's put our test code into
myapp/tests/__init.py here.

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

In this TestCase, we can test a behavior of
``myapp.models.Comment``. You don't need to care about setting up
stubs like DatastoreFileStub. Isn't it very simple?


Using werkzeug.Client for testing views
---------------------------------------

Next, let's test our views. To do so, we can use ``werkzeug.Client``.

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

You can test your views by ``werkzeug.Client``. Currently, there is no
handy way for parsing Response (in above example, I use re module for
this), so you need to do this manually.

.. seealso:: `Werkzeug test utitilies <http://werkzeug.pocoo.org/documentation/0.5.1/test.html>`_

Here is an output of these tests. In this example, we can see the test
names by using ``-v2`` option.

.. code-block:: bash

  $ python manage.py test -v2
  Running on Kay-0.3.0
  test_model (myapp.tests.ModelTest) ... ok
  test_post (myapp.tests.MyappTestCase) ... ok

  ----------------------------------------------------------------------
  Ran 2 tests in 0.093s

  OK
