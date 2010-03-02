==========
Middleware
==========

Middleware is a framework of hooks into Kay's request/response processing.
It's a light, low-level "plugin" system for globally altering Kay's input
and/or output.

Each middleware component is responsible for doing some specific function. For
example, Kay includes a middleware component, ``AuthenticationMiddleware``, that adds
the authentication mechanism to your applications.

This document explains how middleware works, how you activate middleware, and
how to write your own middleware. Kay ships with some built-in middleware
you can use right out of the box; they're documented in the :doc:`builtin-middleware`.

Activating middleware
=====================

To activate a middleware component, add it to the :attr:`settings.MIDDLEWARE_CLASSES`
list in your Kay settings. In ``MIDDLEWARE_CLASSES``, each middleware
component is represented by a string: the full Python path to the middleware's
class name. For example, here's the default ``MIDDLEWARE_CLASSES``
created by ``manage.py startproject``::

    MIDDLEWARE_CLASSES = (
        'kay.auth.middleware.AuthenticationMiddleware',
    )

During the request phases (:meth:`process_request` and :meth:`process_view`
middleware), Kay applies middleware in the order it's defined in
:attr:`settings.MIDDLEWARE_CLASSES`, top-down. During the response phases
(:meth:`process_response` and :meth:`process_exception` middleware), the
classes are applied in reverse order, from the bottom up. You can think of it
like an onion: each middleware class is a "layer" that wraps the view:

A Kay installation doesn't require any middleware -- e.g.,
:attr:`settings.MIDDLEWARE_CLASSES` can be empty, if you'd like.

Writing your own middleware
===========================

Writing your own middleware is easy. Each middleware component is a single
Python class that defines one or more of the following methods:

.. _request-middleware:

``process_request``
-------------------

.. method:: process_request(self, request)

``request`` is an :class:`werkzeug.Request` object. This method is
called on each request, before Kay decides which view to execute.

``process_request()`` should return either ``None`` or an
:class:`werkzeug.Response` object. If it returns ``None``, Kay will
continue processing this request, executing any other middleware and, then, the
appropriate view. If it returns an :class:`werkzeug.Response` object,
Kay won't bother calling ANY other request, view or exception middleware, or
the appropriate view; it'll return that :class:`werkzeug.Response`.
Response middleware is always called on every response.

.. _view-middleware:

``process_view``
----------------

.. method:: process_view(self, request, view_func, view_args, view_kwargs)

``request`` is an :class:`werkzeug.Request` object. ``view_func`` is
the Python function that Kay is about to use. (It's the actual function
object, not the name of the function as a string.) ``view_args`` is a list of
positional arguments that will be passed to the view, and ``view_kwargs`` is a
dictionary of keyword arguments that will be passed to the view. Neither
``view_args`` nor ``view_kwargs`` include the first view argument
(``request``).

``process_view()`` is called just before Kay calls the view. It should
return either ``None`` or an :class:`werkzeug.Response` object. If it
returns ``None``, Kay will continue processing this request, executing any
other ``process_view()`` middleware and, then, the appropriate view. If it
returns an :class:`werkzeug.Response` object, Kay won't bother
calling ANY other request, view or exception middleware, or the appropriate
view; it'll return that :class:`werkzeug.Response`. Response
middleware is always called on every response.

.. _response-middleware:

``process_response``
--------------------

.. method:: process_response(self, request, response)

``request`` is an :class:`werkzeug.Request` object. ``response`` is the
:class:`werkzeug.Response` object returned by a Kay view.

``process_response()`` must return an :class:`werkzeug.Response`
object. It could alter the given ``response``, or it could create and return a
brand-new :class:`werkzeug.Response`.

Unlike the ``process_request()`` and ``process_view()`` methods, the
``process_response()`` method is always called, even if the ``process_request()``
and ``process_view()`` methods of the same middleware class were skipped because
an earlier middleware method returned an :class:`werkzeug.Response`
(this means that your ``process_response()`` method cannot rely on setup done in
``process_request()``, for example). In addition, during the response phase the
classes are applied in reverse order, from the bottom up. This means classes
defined at the end of :attr:`settings.MIDDLEWARE_CLASSES` will be run first.

.. _exception-middleware:

``process_exception``
---------------------

.. method:: process_exception(self, request, exception)

``request`` is an :class:`werkzeug.Request` object. ``exception`` is an
``Exception`` object raised by the view function.

Kay calls ``process_exception()`` when a view raises an exception.
``process_exception()`` should return either ``None`` or an
:class:`werkzeug.Response` object. If it returns an
:class:`werkzeug.Response` object, the response will be returned to
the browser. Otherwise, default exception handling kicks in.

Again, middleware are run in reverse order during the response phase, which
includes ``process_exception``. If an exception middleware return a response,
the middleware classes above that middleware will not be called at all.

``__init__``
------------

Most middleware classes won't need an initializer since middleware classes are
essentially placeholders for the ``process_*`` methods. If you do need some
global state you may use ``__init__`` to set up. However, keep in mind a couple
of caveats:

    * Kay initializes your middleware without any arguments, so you can't
      define ``__init__`` as requiring any arguments.

    * Unlike the ``process_*`` methods which get called once per request,
      ``__init__`` gets called only *once*, when the web server starts up.

Marking middleware as unused
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's sometimes useful to determine at run-time whether a piece of middleware
should be used. In these cases, your middleware's ``__init__`` method may raise
``kay.exceptions.MiddlewareNotUsed``. Kay will then remove that
piece of middleware from the middleware process.

Guidelines
----------

    * Middleware classes don't have to subclass anything.

    * The middleware class can live anywhere on your Python path. All Kay
      cares about is that the :attr:`settings.MIDDLEWARE_CLASSES` setting includes
      the path to it.

    * Feel free to look at :doc:`builtin-middleware` for examples.

    * If you write a middleware component that you think would be useful to
      other people, contribute to the community! `Let us know
      <http://groups.google.com/group/kay-users>`_, and we'll consider adding it to Kay.
