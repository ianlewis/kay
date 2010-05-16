=============
Using session
=============

Overview
--------

Kay has a capability for handling anonymous session. Once you enable
this capability, every ``request`` object has session attribute
automatically. You can store any data(as long as it can be pickled) in
this session.

Configuration
-------------

You need to put ``kay.sessions`` application into
:attr:`settings.INSTALLED_APPS` and put
``kay.sessions.middleware.SessionMiddleware`` into
:attr:`settings.MIDDLEWARE_CLASSES`. You can choose how to store
session data by setting :attr:`settings.SESSION_STORE` value. The
valid value is one of ``kay.sessions.sessionstore.GAESessionStore``
and ``kay.session.sessionstore.SecureCookieSessionStore``.

.. code-block:: python

  SESSION_STORE = 'kay.sessions.sessionstore.GAESessionStore'
  #SESSION_STORE = 'kay.sessions.sessionstore.SecureCookieSessionStore'

  INSTALLED_APPS = (
    'kay.sessions',
    'myapp',
  )

  # ...

  MIDDLEWARE_CLASSES = (
    'kay.sessions.middleware.SessionMiddleware',
    'kay.auth.middleware.GoogleAuthenticationMiddleware',
  )

When using ``GAESessionStore``, session data will be stored in Datastore, and only the session id will be passed to user's browser as a cookie. When using ``SecureCookieSessionStore``, all the session data will be stored in a single cookie in user's browser, so you should store only small data as ids if you use ``SecureCookieSessionStore``.

Decorator
---------

Once kay has ``kay.sessions.decorators.no_session`` decorater, but you
don't need to use it any more. The attribute value of request.session
is evaluated lazily, so there is no datastore/memcache access unless
you use session's value.


Purging old sessions
--------------------

If you use ``GAESessionStore``, you should delete expired old session
data. There is a view for purging old sessions at
``kay.sessions.views.purge_old_sessions``. This view is bound to the
URL ``/sessions/purge_old_sessions`` by default. If you want to purge
old session data, you need to call this view by cron or something
similar periodically. Here is a sample cron settings for this:

cron.yaml

.. code-block:: yaml

  cron:
  - description: purge old session data
    url: /sessions/purge_old_sessions
    schedule: every 1 hours


How to store data into session
------------------------------

Treat ``request.session`` as if its just a dict. Here is an example
view implementation of a simple counter.

.. code-block:: python

  def index(request):
    count = request.session.get('count', 0) + 1
    request.session['count'] = count
    #...
    #...

