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


You can handle i18n like following. For the details of i18n, please
refer to :doc:`i18n`.

.. code-block:: bash

   $ python manage.py extract_messages hello
   $ python manage.py add_translations hello -l ja
   $ vi hello/i18n/ja/LC_MESSAGES/messages.po
   $ python manage.py compile_translations hello

You can also merge newly added catalogue into your translations as
follows.

.. code-block:: bash

   $ python manage.py extract_messages hello
   $ python manage.py update_translations hello -l ja
   $ vi hello/i18n/ja/LC_MESSAGES/messages.po
   $ python manage.py compile_translations hello

Shell tools
-----------

Invoking ``python manage.py shell`` gives you python (or ipython if
available) shell session with the same DatastoreFileStub settings of
local dev server. For the details of manage.py commands, please
refer to :doc:`manage_py`.

**Note:**

  The local dev server reads datastore data file only on startup. So,
  the dev server will never notice about the datastore operation on
  your bash session. You must restart your dev server for
  reflecting the result of the bash sessions.

Invoking ``python manage.py rshell`` is the same as above except for
using RemoteDatastore stub. You can access the data on the
production server.

**Note:**
  
Please be careful when you use this feature as you will be
interacting with live data.

Datastore
---------

You must use GAE models directly. You can use kay.utils.forms for
form handling. You can construct a form automatically from the model
definition with kay.utils.forms.modelform.ModelForm. For the details
of how to use forms, please refer to :doc:`forms-usage`.

By default, db.Model.kind() returns ('model's app name' + _ + 'model
name').lower(). So when you see the management bash, there will
be 'appname_modelname' style kind names . Please don't be surprised
with those names.

You can change this behaviour by settings ADD_APP_PREFIX_TO_KIND to
False in your settings.py.

The experimental db_hook feature is now available in kay's repository.
To use this feature, you have to set USE_DB_HOOK to True in your top level
settings.py file. Also you have to register your hooks beforehands
somewhere in your code. I recommend you to do this in
appname/__init__.py because Kay always load this file on startup as
long as appname is on your INSTALLED_APPS. Here is an example for
registering a hook that logs dumpped represantation of the saved
entry and whether this operation is creating a new entity or
updating an existing entity.

.. code-block:: python

  import logging

  from kay.utils import db_hook
  from kay.utils.db_hook import put_type

  from hoge.models import Entry

  def log_instance(entity, put_type_id):
    from kay.utils.repr import dump
    logging.info(dump(entity))
    logging.info("put_type: %s" % put_type.get_name(put_type_id))

  register_post_save_hook(log_instance, Entry)


Forms
-----

To define form class, you will need to define a class that extends
kay.utils.forms.Form. For example the code bellow will give you the
form contains two text fields with different validators.

.. code-block:: python

    from kay.utils.forms import Form
    class PersonForm(Form):
      name = TextField(required=True)
      age = IntegerField()


You can use this form in your view like following.
 
.. code-block:: python

    from forms import PersonForm
    form = PersonForm()
    if request.method == 'POST'
      if form.validate(request.form, request.files):
        name = form['name']
	age = form['age']
        do something with valid form ...
      else:
        do something with invalid form ...


You can also use ModelForm to create a form automatically from Model
class.

.. code-block:: python

    from google.appengine.ext import db

    class MyModel(db.Model):
      name = db.StringProperty(required=True)
      age = db.IntegerProperty()

    from kay.utils.forms.modelform import ModelForm

    class MyForm(ModelForm):
      class Meta:
        model = MyModel

Questions and Bug Reports
-------------------------

* Please visit Kay framework google group.
  http://groups.google.com/group/kay-users
  
* Or, contact the project leader directly.
  Takashi Matsuo <tmatsuo@candit.jp>

* Code site
  http://code.google.com/p/kay-framework/

Have fun!
