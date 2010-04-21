====================
Using authentication
====================

Overview
--------

Google App Engine has a very nice default auth mechanism using google
account or google apps account. You can use this capability with
extensible manner with ``AuthenticationMiddleware`` and
``kay.auth.backends.googleaccount.GoogleBackend``. You can also use
username and password information stored in the app engine datastore.

Enabling Authentication middleware
----------------------------------

To use Kay's authentication mechanism, you need to add
``kay.auth.middleware.AuthenticationMiddleware`` to
:attr:`settings.MIDDLEWARE_CLASSES`.

Using google account authentication
-----------------------------------

By default, :attr:`settings.AUTH_USER_BACKEND` is set to
``kay.auth.backends.googleaccount.GoogleBackend``. This backend is for
authentication using google account or google apps account. If a user
logs into your app first time, an information of the user is stored as
``kay.auth.models.GoogleUser`` entity (It's just a default setting, it
is also customizable) in the GAE datastore. You can use this
middleware and backend combination without using session capability.

To customize user model, you need to define new class extended from
``kay.auth.models.GoogleUser``, add any required properties to it, and
set the name of your new class to :attr:`settings.AUTH_USER_MODEL`.

.. code-block:: python

  MIDDLEWARE_CLASSES = (
    'kay.auth.middleware.AuthenticationMiddleware',
  )
  AUTH_USER_BACKEND = 'kay.auth.backends.googleaccount.GoogleBackend'
  AUTH_USER_MODEL = 'kay.auth.models.GoogleUser'

Using datastore authentication
------------------------------

To use datastore authentication, you need to set
``kay.auth.models.DatastoreUser`` (or a classname that is extended
from it) to :attr:`settings.AUTH_USER_MODEL` and
``kay.auth.backends.datastore.DatastoreBackend`` to
:attr:`settings.AUTH_USER_BACKEND`. AuthenticationMiddleware must be
placed under SessionMiddleware that is mandatry for this middleware.
You also need to add ``kay.auth`` to :attr:`settings.INSTALLED_APPS`.

.. code-block:: python

  INSTALLED_APPS = (
    'kay.auth',
  )
  MIDDLEWARE_CLASSES = (
    'kay.sessions.middleware.SessionMiddleware',
    'kay.auth.middleware.AuthenticationMiddleware',
  )
  AUTH_USER_BACKEND = 'kay.auth.backends.datastore.DatastoreBackend'
  AUTH_USER_MODEL = 'kay.auth.models.DatastoreUser'

Helper functions and decorators
-------------------------------

There are helper functions in ``kay.utils`` module:
``create_logout_url`` and ``create_login_url``. These functions are
automatically imported into templates' rendering context. So you can
use these functions in your templates just like:

.. code-block:: html

  {% if request.user.is_anonymous() %}
    <a href="{{ create_login_url() }}">login</a>
  {% else %}
    Hello {{ request.user }}! <a href="{{ create_logout_url() }}">logout</a>
  {% endif %}

There are decorators in ``kay.auth.decorators`` module:
``login_required`` and ``admin_required``. You can decorate any view
of yours with these decorators just like:

.. code-block:: python

  @login_required
  def user_profile(request):
    """ This is a view for detailed information of the user's profile. 
    """
    ...
    ...
    
  @admin_required
  def manage_users(request):
    """ This is a view for user management.
    """
    ...
    ...

Creating a new user
-------------------

``kay.auth.create_new_user`` is a function for creating new user. If
there is a user with the same user_name, this function raises
``kay.auth.DuplicateKeyError``. If succeeded, it returns a newly
created user object.

.. code-block:: python

   from kay.auth import create_new_user
   user_name = 'hoge'
   password = 'hoge'
   new_user = create_new_user(user_name, password, is_admin=is_admin)

You can also use ``manage.py create_user`` command like following:

.. code-block:: bash

   $ python manage.py create_user hoge

This commands will ask you a new password for this user.

Use loginbox
------------

To use loginbox, you can add ``kay.auth.context_processors.login_box``
to :attr:`settings.CONTEXT_PROCESSORS`, and import ``render_loginbox``
macro from ``auth/macros.html`` in your template, and use this macro
whereever you want. Here is an example usage:

settings.py:

.. code-block:: python

   CONTEXT_PROCESSORS = (
     'kay.context_processors.request',
     'kay.context_processors.url_functions',
     'kay.context_processors.media_url',
     'kay.auth.context_processors.login_box'
   )

template:

.. code-block:: html

   {% from "auth/macros.html" import render_loginbox with context %}

   {% if request.user.is_anonymous() %}
     {{ render_loginbox() }}
   {% else %}
     Hello {{ request.user }}! <a href="{{ create_logout_url() }}">logout</a>
   {% endif %}


Using datastore authentication on an owned domain
-------------------------------------------------

TODO