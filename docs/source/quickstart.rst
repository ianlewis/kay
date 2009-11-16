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

If you'd like to use MacPort's python25, you also need to install
following software:

* py25-hashlib
* py25-socket-ssl
* py25-pil
* py25-ipython (recommended)

This time we use the Kay repository version. To do so, you need
Mercurial installed on your system.

* mercurial

You can clone Kay repository version as follows.

.. code-block:: bash

  $ hg clone https://kay-framework.googlecode.com/hg/ kay

If you'd like to use Kay release version, download the newest version from
http://code.google.com/p/kay-framework/downloads/list and extract it as follows:

.. code-block:: bash

   $ tar zxvf kay-VERSION.tar.gz


If you installl an appengine SDK zip package, you need to create a
symlink beforehand like following:

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

On the platform supports symbolic link system, ``kay`` directory and
the symblic link to ``manage.py`` will be created.  If you move them
to another directory, your project may not work.  In that case you
need create the symlink again.


Create an application
---------------------

Go into ``myproject`` directory and create an application. Following
example shows how to create ``myappp`` application.

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

After the application is created, you need to edit ``settings.py`` for
registering it to the project. You can also register it to
``APP_MOUNT_POINTS`` for changing which URL this application is
mounted at if you need to. The following example shows you how to
mount it at the root URL(/).  If you don't edit ``APP_MOUNT_POINTS``,
the application will be mounted at the URL that has its' own name with
leading slash like ``/myapp`` or ``/auth``.  In this example, we
registered ``kay.auth`` application as well.

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


As you know, ``INSTALLED_APPS`` is a tuple and ``APP_MOUNT_POINTS`` is
a dict.

Move your application
---------------------

Let's run the application you've just created. You can run a
development server with a following command:

.. code-block:: bash

  $ python manage.py runserver
  INFO     2009-08-04 05:48:21,339 appengine_rpc.py:157] Server: appengine.google.com
  ...
  ...
  INFO     ... Running application myproject on port 8080: http://localhost:8080

Then, launch your web browser and go to http://localhost:8080/. You
should see `"hello"` or `"こんにちは"`.


Upload to GAE
-------------

Edit the ``app.yaml`` file, then change the value of the
``application:`` to your registered application ID.  To upload your
application to GAE, you can execute a following command.

.. code-block:: bash

  $ python manage.py appcfg update

If succesfully uploaded, now you can see your application running on
GAE at http://your-appid.appspot.com/.


Template/View
-------------

Let's look at the default view and the template.


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

	
One default view is already defined.
:func:`kay.utils.render_to_response()` function receives a template's
name as the first argument. You can pass a dictionary as the second
argument. That dictionary will be passed to the template.  ``_()``
function marks strings for i18n extraction and replaces with
transalted text when pages are rendered.  ``myapp/index.html``
template's real path on your system is ``myapp/templates/index.html``
(Note that ``/templates/`` is nestled).


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

{{ message }} will be replaced with a value in the context dictionally
with a key ``message``.  


URL Mapping
-----------

Next, look at the file that configures the mapping between URLs and
views.

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


Kay will automatically collect and configure the ``make_rules()``
funtion and the ``all_views`` dictionary defined in ``urls.py`` in
apps directory.

The ``make_rules()`` function binds the ``'/'`` URL to the
``'myapp/index'`` endpoint.  The ``all_views`` dictionary binds the
``'myapp/index'`` endpoint to the ``myapp.views.index`` function.

Thus it will allow the application to call ``myapp.views.index``, when
``'/'`` is accessed.

``'/'`` -> ``'myapp/index'`` -> ``myapp.views.index``


User Authentication
-------------------

There are some ways how to authenticate users. Now we will
authenticate users with Google Accounts.  By default, ``settings.py``
is configured to use Google Account Authenticaion.  So you don't need
to edit ``settings.py`` in this case.

If you edit ``myapp/templates/index.html`` as follows, you can use
user authentication.

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

If the user hasn't signed in, above code shows a link to login form.
Otherwise it shows the user's Email address and a logout link.

Let's try this user authentication code both on the development
environment and GAE.

For now, any user will be able to browse ``myapp.index`` without
singning in. How can we allow users to browse this page only when they
are signed in?

You can use a decorator to do so, as follows:

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.views
  # ...
  # ...
  # Create your views here.

  @login_required
  def index(request):
    return render_to_response('myapp/index.html', {'message': _('Hello')})

If you decorate the view with a ``login_required`` decorator, only
signed-in users will be able to browse the page.

Once you check the operation, remove this decorator.


Model Definition
----------------

Now let's make the application to let users posting comments and to
store it into the datastore. Firstly let's define a model to store
comments.

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

You can define a model by making a Python class that inherits from the
``google.appengine.ext.db.Model`` class.  You can also define
properties by putting class attributes on the model class.  Define the
``user`` property to store comment's owner, ``body`` property for
storing the content, and ``created`` property stores the posted date.

Let's store data in this model. You can use Kay's shell tool for it.

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
Note that if you forget to run ``put()``, you cannot have data saved.
Additionally, the data you stored by shell tool won't appear on the
dev server until you restart the dev server. Check if the data was
saved by restarting the development server and check following URL:
http://localhost:8080/_ah/admin/


Display Data
------------

Let's display the Comment you've just stored. Edit two files as
follows:

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
``Comment.all().order('-created').fetch(100)`` returns a list contains
the latest 100 comments from datastore. We pass this list to
:func:`kay.utils.render_to_response()`.

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

Add a new div element next to the ``message`` line. The code between
``{% for ... %}`` and ``{% endfor %}`` is a loop. In this loop, we
display just ``comment.body``.


Comment Form
------------

Let's add a feature to submit comments. Create a new file named
``forms.py`` for a html form.

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


You can use ``request.form`` to access the POST value,
``request.args`` to access the GET parameters, and ``request.files``
to access to the uploaded files.

myapp/templates/index.html

.. code-block:: html

  <div>
  {{ form()|safe }}
  </div>

Now, you can post a comment. The username of the poster will be also
displayed beside it.
