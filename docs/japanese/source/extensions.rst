===============
kay.ext package
===============

.. Note::

   This feature is still an experimental. The implementation might
   change in the future.

Let me introduce you some of useful packages from ``kay.ext`` package.

.. module:: kay.ext

kay.ext.nuke
============

nuke is a small tool for wipe all of your data in one action.

.. module:: kay.ext.nuke

To use kay.ext.nuke, firstly you need to retrieve bulkupdate copy from `github repository <http://github.com/arachnid/bulkupdate>`_, put it under your project directory, add ``kay.ext.nuke`` to your :attr:`settings.INSTALLED_APPS` variable, and add these few lines to your ``app.yaml`` file.

.. code-block:: yaml

  admin_console:
    pages:
    - name: Bulk Update Jobs
      url: /_ah/bulkupdate/admin/
    - name: Nuke
      url: /_ah/nuke/
  
  handlers:
  - url: /_ah/nuke/.*
    script: kay/main.py
    login: admin
  
  - url: /_ah/bulkupdate/admin/.*
    script: bulkupdate/handler.py
    login: admin


Then you will see ``Nuke`` menu on your admin console, or you can just visit ``/_ah/nuke`` directly.


kay.ext.gaema
=============

kay.ext.gaema is a package for supporting authentication using some
social services. Currently following services are supported.

* google OpenID
* google OpenID/OAuth Hybrid
* Twitter OAuth
* Facebook Connect
* Yahoo OpenID

``kay.ext.gaema.services`` module has constants for these service
names:

* GOOG_OPENID
* GOOG_HYBRID
* TWITTER
* FACEBOOK
* YAHOO

All of following functions have ``service`` as its first argument, a
value of ``service`` must be one of service names above.

To use twitter or facebook, you need to register your application on
the service's website, and set your keys to
:attr:`settings.GAEMA_SECRETS` dictionary.

kay.ext.gaema.utils package has following functions.

.. module:: kay.ext.gaema.utils

.. function:: create_gaema_login_url(service, nexturl)

  A function for creating login_url for a particular social
  service. User will be redirected to the url specified by ``nexturl``
  argument after successfully logged in.

.. function:: create_gaema_logout_url(service, nexturl)

  A function for creating logout_url for a particular social
  service. User will be redirected to the url specified by ``nexturl``
  argument after successfully logged out.

.. function:: get_gaema_user(service)

  A function for retrieving current user's information as a
  dictionary. If the user is not signed in with a social service, it
  returns ``None``.


kay.ext.gaema.decorators package has following decorators.

.. module:: kay.ext.gaema.decorators

.. function:: gaema_login_required(*services)

  A decorator for restricting access to a view only to users who is
  signed in with particular social service. You can pass any number of
  service.


Here is a simple example that shows how to authenticate users with
twitter OAuth. Firstly, you need to register your application on
`Twitter's website <http://twitter.com/apps>`_, and set a key and
secret from twitter to :attr:`settings.GAEMA_SECRETS` as well as
:attr:`settings.INSTALLED_APPS`, and activate
``kay.sessions.middleware.SessionMiddleware`` as follows:

.. code-block:: python

  INSTALLED_APPS = (
    'myapp',
    'kay.ext.gaema',
  )

  GAEMA_SECRETS = {
    "twitter_consumer_key": "hogehogehogehogehogehoge",
    "twitter_consumer_secret": "fugafugafugafugafugafugafugafuga",
  }

  MIDDLEWARE_CLASSES = (
    'kay.sessions.middleware.SessionMiddleware',
  )

Here is an example for views:

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.views

  import logging

  from werkzeug import Response
  from kay.ext.gaema.utils import (
    create_gaema_login_url, create_gaema_logout_url, get_gaema_user
  )
  from kay.ext.gaema.decorators import gaema_login_required
  from kay.ext.gaema.services import TWITTER
  from kay.utils import (
    render_to_response, url_for
  )

  # Create your views here.

  def index(request):
    gaema_login_url = create_gaema_login_url(TWITTER,
					     url_for("myapp/secret"))
    return render_to_response('myapp/index.html',
			      {'message': 'Hello',
			       'gaema_login_url': gaema_login_url})

  @gaema_login_required(TWITTER)
  def secret(request):
    user = get_gaema_user(TWITTER)
    gaema_logout_url = create_gaema_logout_url(TWITTER,
					       url_for("myapp/index"))
    return render_to_response('myapp/secret.html',
			      {'user': user,
			       'gaema_logout_url': gaema_logout_url})


