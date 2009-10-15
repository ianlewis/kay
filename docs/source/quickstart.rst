==============
Kay Quickstart
==============

Create a symlink for appengine SDK if neccessary
------------------------------------------------

If you installed a zip package of appengine SDK, you need to create
a symlink beforehand like following:

.. code-block:: bash

   $ sudo ln -s /some/whare/google_appengine /usr/local/google_appengine    


Let's Get Started
-----------

If you'd like to use kay's development version, you can create a new
project by following these steps:

.. code-block:: bash

   $ hg clone https://kay-framework.googlecode.com/hg/ kay
   $ python kay/manage.py startproject myproject
   $ cd myproject

If you'd like to use kay release version, first, download the newest
version from http://code.google.com/p/kay-framework/downloads/list,
and do as follows:

.. code-block:: bash

   $ tar zxvf kay-VERSION.tar.gz
   $ python kay-VERSION/manage.py startproject myproject
   $ cd myproject


Second, you can create your first application with the following command.

.. code-block:: bash

   $ python manage.py startapp hello
   $ vi settings.py

Now you have to add 'hello' to the INSTALLED_APPS tupple in the
settings.py. For the details of how to define urls and views for your
application, please refer to :doc:`urlmapping`.

settings.py:
.. code-block:: python

  INSTALLED_APPS = (
    'hello'
  )

Run your application

.. code-block:: bash

  $ python manage.py runserver


You can access your first application on the url:

    http://localhost:8080/hello/

Upload your application

.. code-block:: bash

  $ python manage.py appcfg update

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
------------------------

* Please visit Kay framework google group.
  http://groups.google.com/group/kay-users
  
* Or, contact the project leader directly.
  Takashi Matsuo <tmatsuo@candit.jp>

* Code site
  http://code.google.com/p/kay-framework/

Have fun!
