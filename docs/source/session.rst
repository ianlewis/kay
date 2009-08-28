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

You need to put ``kay.sessions`` application into ``INSTALLED_APPS``
and put ``kay.sessions.middleware.SessionMiddleware`` into
``MIDDLEWARE_CLASSES`` in your ``settings.py`` file.

.. code-block:: python

  INSTALLED_APPS = (
    'kay.sessions',
    'myapp',
  )

  # ...

  MIDDLEWARE_CLASSES = (
    'kay.sessions.middleware.SessionMiddleware',
    'kay.auth.middleware.GoogleAuthenticationMiddleware',
  )

Decorator
---------

There is a decorator for marking particular view not to use session
capability at ``kay.sessions.decorators.no_session``. You can mark any
view not to use session capability like following:

.. code-block:: python

  from kay.sessions.decorators import no_session

  def custom_page(request):
    """ This view use session capability.
    """
    #...
    #...

  @no_session
  def public_page(request):
    """ This view doesn't use session
    """
    #...
    #...


Purging old sessions
--------------------

There is a view for purging old sessions at
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

