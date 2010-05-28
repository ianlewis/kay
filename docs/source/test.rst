=============
Running Tests
=============

Overview
--------

You can test your applications by invoking :option:`manage.py test -t`
or ``manage.py test`` without any options. You are highly recommended
to subclassing ``kay.ext.testutils.gae_test_base.GAETestBase`` for
your TestCase classes. GAETestBase will take care of setting up
environments for your tests according to your configuration. Basically
you can configure a behavior of GAETestBase class by defining class
attributes on your test cases.

You can run your tests by::

  * invoking test subcommand by typing ``python manage.py test``
  * visiting ``/_ah/test`` on the development server or the
    production server either

.. Note::

   When you run your tests on the production server, all the tests
   will be invoked in parallel, so you need to write your test
   function independent to other test functions.

Your first test
---------------

``manage.py test`` automatically collects subclasses of TestCase from
tests module under your APP_DIR. So let's put our test code into
myapp/tests/__init.py here.

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

In this TestCase, we can test a behavior of
``myapp.models.Comment``. You don't need to care about setting up
stubs like DatastoreFileStub. Isn't it very simple?

Configurations
--------------

You can configure a behavior of GAETestBase by setting the class
attributes on your test case. The default value of all following
attributes is ``False`` except for ``KIND_PREFIX_IN_TEST`` that has a
default value ``'t'``.

* USE_PRODUCTION_STUBS

  If this attribute is set to ``True``, GAETestBase uses datastore API
  on the production server instead of datastore_file_stub when you run
  your tests on the production server.

* USE_REMOTE_STUBS

  If this attribute is set to ``True``, GAETestBase uses datastore API
  via remote_api when you run your tests via manage.py.

* CLEANUP_USED_KIND

  If this attribute is set to ``True``, GAETestBase will delete all
  the entities which your tests accessed thru the tests.

* KIND_NAME_UNSWAPPED

  If this attribute is set to ``True``, GAETestBase will use original
  kind names instead of prefixed one.

* KIND_PREFIX_IN_TEST

  By default, GAETestBase adds ``t_`` prefix to kind value of all
  models. You can change this prefix by this attirbute. If you set
  this to ``test``, the prefix will be ``test_``.

For example, you don't need the ``tearDown()`` method of your first
test any more if you set ``CLEANUP_USED_KIND`` to ``True`` because
GAETestBase will take care of cleanup.

Another example, You can also run your test on the production
environment if you set ``USE_PRODUCTION_STUBS`` to ``True``.

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


Using werkzeug.Client for testing views
---------------------------------------

Next, let's test our views. To do so, we can use ``werkzeug.Client``
class and ``kay.utils.test`` module.

myapp/tests/__init__.py:

.. code-block:: python

  from google.appengine.ext import db
  from werkzeug import BaseResponse, Client, Request
  from kay.app import get_application
  from kay.utils.test import (
    init_recording, get_last_context, get_last_template, disable_recording,
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

You can test your views by ``werkzeug.Client``. You can use
``get_last_template`` and ``get_last_context`` for getting a name of a
last-used template and last-used context after invoking
``init_recording``.

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

Output debug log to a specified file
------------------------------------

You can configure logging for seeing application's log as follows:

.. code-block:: python

  import logging
  logging.basicConfig(filename="test-debug.log", level=logging.DEBUG)

You can also put similar lines to individual setUp methods:

.. code-block:: python

  import logging

  from google.appengine.ext import db

  from werkzeug import BaseResponse, Client, Request
  from kay.app import get_application
  from kay.ext.testutils.gae_test_base import GAETestBase

  from myapp.models import Comment

  class MyappTestCase(GAETestBase):
    def setUp(self):
      logging.basicConfig(filename="test-debug.log", level=logging.DEBUG)
      app = get_application()
      self.client = Client(app, BaseResponse)
    # ..
    # ..
