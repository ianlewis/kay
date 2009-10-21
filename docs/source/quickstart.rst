==============
Kay Quickstart
==============

Firstly this tutorial gives you the way to create an simple BBS.

Preperation
-----------

Please install the softwares below.

* Python-2.5
* App Engine SDK/Python
* Kay Framework
* ipython (recommended)

If you'd like to use MacPort's python25 in macports, you also need to install the softwares below.

* py25-hashlib
* py25-socket-ssl
* py25-pil
* py25-ipython (recommended)

This time we use the Kay repository version. To do that you need Mercurial.

* mercurial

You can clone it as follows.

.. code-block:: bash

  $ hg clone https://kay-framework.googlecode.com/hg/ kay

If you'd like to use Kay release version, download the newest
version from http://code.google.com/p/kay-framework/downloads/list and extract it as follows:

.. code-block:: bash

   $ tar zxvf kay-VERSION.tar.gz


If you installed a zip package of appengine SDK, you need to create
a symlink beforehand like following:

.. code-block:: bash

   $ sudo ln -s /some/whare/google_appengine /usr/local/google_appengine    


Start a new project
-------------------

Create the skelton of the project directory with Kay's ``manage.py`` script.

.. code-block:: bash

   $ python kay/manage.py startproject myproject
   $ tree myproject
   myproject
   |-- app.yaml
   |-- kay -> /Users/tmatsuo/work/tmp/kay/kay
   |-- manage.py -> /Users/tmatsuo/work/tmp/kay/manage.py
   |-- settings.py
   `-- urls.py

   1 directory, 4 files

On the platform supports symbolic link system, ``kay`` directory and the symblic link to ``manage.py`` will be created. If you move them to another directory, your project may not work. In that case you need create it again.

Create an application
---------------------

Go into ``myproject`` directory and let's create an application. Following example shows how to create ``myappp`` application.

.. code-block:: bash

   $ cd myproject
   $ python manage.py startapp myapp
   $ tree myapp
   myapp
   |-- __init__.py
   |-- models.py
   |-- templates
   |   `-- index.html
   |-- urls.py
   `-- views.py

   1 directory, 5 files

The application have been created, you then edit ``settings.py`` to register it to the project. If you need you can also register it to ``APP_MOUNT_POINTS``. The following example mount it to the root URL.
If you don't edit ``APP_MOUNT_POINTS``, the application will be mounted on the URL has its' own name like ``/myapp``. Additionaly we also regist ``kay.auth`` application.

settings.py

.. code-block:: python

  #$/usr/bin/python
  #..
  #..

  INSTALLED_APPS = (
    'kay.auth',
    'myapp',
  )

  APP_MOUNT_POINTS = {
    'myapp': '/',
  }


As you know, ``INSTALLED_APPS`` is a tuple and ``APP_MOUNT_POINTS`` is a dict.

Move your application
---------------------

Let's run the application you created. The following command will run a development server.

.. code-block:: bash

  $ python manage.py runserver
  INFO     2009-08-04 05:48:21,339 appengine_rpc.py:157] Server: appengine.google.com
  ...
  ...
  INFO     ... Running application myproject on port 8080: http://localhost:8080

Now, call up a browser and go to http://localhost:8080/. You should see `"hello"` or `"こんにちは"`.


Upload to GAE
-------------

In order to upload your application to GAE you need set the ``appid`` to ``application`` in ``app.yaml`` and use the following command.

.. code-block:: bash

  $ python manage.py appcfg update

If uploading is successed you can access to http://your-appid.appspot.com/


Template/View
-------------

Let's see the default view and template.


myapp/views.py

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.views

  import logging

  from google.appengine.api import users
  from google.appengine.api import memcache
  from werkzeug import (
    unescape, redirect, Response,
  )
  from werkzeug.exceptions import (
    NotFound, MethodNotAllowed, BadRequest
  )

  from kay.utils import (
    render_to_response, reverse,
    get_by_key_name_or_404, get_by_id_or_404,
    to_utc, to_local_timezone, url_for, raise_on_dev
  )
  from kay.i18n import gettext as _
  from kay.auth.decorators import login_required

  # Create your views here.

  def index(request):
    return render_to_response('myapp/index.html', {'message': _('Hello')})

	
One default view is defined. ``render_to_response`` function receives the template's name as the first argument. You can pass an dictionary which is passed to the template as second argument to it. The ``_()`` function marks strings for i18n and works when the page is displayed. The template indicated by ``myapp/index.html`` actually exists ``myapp/templates/index.html`` (Note that ``/templates/`` is nestled).

myapp/templates/index.html

.. code-block:: html

  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">
  <html>
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Top Page - myapp</title>
  </head>
  <body>
  {{ message }}
  </body>
  </html>

``message`` that is passed to ``render_to_response`` as the second argument ``render_to_response`` will be displayed in the ``{{ message }}`` field.


URL Mapping
-----------

Next we will see the file that configures the correspondance between URLs and views.

myapp/urls.py

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.urls


  from werkzeug.routing import (
    Map, Rule, Submount,
    EndpointPrefix, RuleTemplate,
  )
  import myapp.views

  def make_rules():
    return [
      EndpointPrefix('myapp/', [
	Rule('/', endpoint='index'),
      ]),
    ]

  all_views = {
    'myapp/index': myapp.views.index,
  }


``make_rules()`` funtion and ``all_views`` dictionary defined in ``urls.py`` will be automatically corrected and configured by Kay.

``make_rules`` corresponds the ``'/'`` URL to the ``'myapp/index'`` endpoint. ``all_views`` corresponds the ``'myapp/index'`` endpoint to the ``myapp.views.index`` function.

These will allow the application to call ``myapp.views.index``,  When ``'/'`` is accessed


User Authentication
-------------------

There are some ways to use user authentication. In this chapter we will use the authentication with Google Account. ``settings.py`` is configured to use Google Account Authenticaion by default. So you don't need to configure any settings.

If you edit ``myapp/templates/index.html`` as follows, you can use user authentication.

.. code-block:: html

  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">
  <html>
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Top Page - myapp</title>
  </head>
  <body>
  <div id="greeting">
  {% if request.user.is_anonymous() %}
  <a href="{{ create_login_url() }}">login</a>
  {% else %}
  Hello {{ request.user }}! <a href="{{ create_logout_url() }}">logout</a>
  {% endif %}
  </div>
  {{ message }}
  </body>
  </html>

Above code shows the link to login form if the user doesn't login, otherwise shows user's Email address and logout link.

Let's try in the development environment and GAE.

In this step, the user can view ``myapp.index`` without login. How can we to allow the user view when s/he logins?

Using decorator as follows enables to do that.

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.views
  # ...
  # ...
  # Create your views here.

  @login_required
  def index(request):
    return render_to_response('myapp/index.html', {'message': _('Hello')})

If you decorate the view with ``login_required`` decorator, you allow the user to view that.

Remove this decorator after checking of the operation,


Model Definition
----------------

Now we will make our application to let us to post comments to datastore. Firstly we will define a model to save a comment.

myapp/models.py

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.models

  from google.appengine.ext import db

  # Create your models here.

  class Comment(db.Model):
    user = db.ReferenceProperty()
    body = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

We define this model by creating the class inherits ``google.appengine.ext.db.Model``. You can define properties by defining class variables. Now we will define to save the user in ``user``, the content in ``body``, and the posted date in ``created``.

Let's save data in this model. You can use Kay shell tool to save data.

.. code-block:: bash

  $ python manage.py shell
  Running on Kay-0.0.0
  In [1]: c1 = Comment(body='Hello, guestbook')
  In [2]: c1.put()
  Out [2]: datastore_types.Key.from_path(u'myapp_comment', 1, _app_id_namespace=u'myproject')
  In [3]: c1.body
  Out[3]: u'Hello, guestbook'
  In [4]: ^D
  Do you really want to exit ([y]/n)? y

^D means Ctrl + D.
Note that If you forget ``put()`` you cannot save data. Check if data was saved by run the development server and go to http://localhost:8080/_ah/admin/


Display Data
------------

Display the Comment you saved lately. Edit 2 files below.


myapp/views.py

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.views
  # ...
  # ...
  from models import Comment

  # Create your views here.

  def index(request):
    comments = Comment.all().order('-created').fetch(100)
    return render_to_response('myapp/index.html',
			      {'message': _('Hello'),
			       'comments': comments})

Don't forget to import the Model class you defined earlier.
``Comment.all().order('-created').fetch(100)`` get latest 100 comments from datastore. And pass the list to ``render_to_response``. Please refer to :func:`kay.utils.render_to_response`.

myapp/templates/index.html

.. code-block:: html

  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">
  <html>
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Top Page - myapp</title>
  </head>
  <body>
  <div id="greeting">
  {% if request.user.is_anonymous() %}
  <a href="{{ create_login_url() }}">login</a>
  {% else %}
  Hello {{ request.user }}! <a href="{{ create_logout_url() }}">logout</a>
  {% endif %}
  </div>
  {{ message }}
  <div>
  {% for comment in comments %}
  <hr/>
  {{ comment.body }}&nbsp;by&nbsp;<i>{{ comment.user }}</i>
  {% endfor %}
  </div>
  </body>
  </html>

Add a new div under the place displays ``messages``.
Between ``{% for ... %}`` and ``{% endfor %}`` is loops. Now we just display ``comment.body``.


Comment Form
------------

Let's make our application to submit comments。Creata a new file named ``forms.py`` for html form.

myapp/forms.py


.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.views
  #...
  #...
  from models import Comment
  from forms import CommentForm

  # Create your views here.

  def index(request):
    comments = Comment.all().order('-created').fetch(100)
    form = CommentForm()
    if request.method == 'POST':
      if form.validate(request.form):
	if request.user.is_authenticated():
	  user = request.user
	else:
	  user = None
	new_comment = Comment(body=form['comment'],user=user)
	new_comment.put()
	return redirect('/')
    return render_to_response('myapp/index.html',
			      {'message': _('Hello'),
			       'comments': comments,
			       'form': form.as_widget()})


You can use ``request.form`` to access the POST value, ``request.args`` to access the GET parameters, and ``request.files`` to access to the uploaded files.

myapp/templates/index.html

.. code-block:: html

  <div>
  {{ form()|safe }}
  </div>

At this point you can post a comment. The name who posted it will be also displayed beside the comment.
