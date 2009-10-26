=============================
Built-in middleware reference
=============================

This document explains all middleware components that come with Kay. For
information on how how to use them and how to write your own middleware, see
the :doc:`middleware`.

Available middleware
====================

Cache middleware
----------------

.. module:: kay.cache.middleware
   :synopsis: Middleware for the site-wide cache.

.. class:: kay.middleware.cache.UpdateCacheMiddleware

Enable the site-wide cache. If these are enabled, each Kay-powered page will
be cached for as long as the :attr:`settings.CACHE_MIDDLEWARE_SECONDS` setting
defines.

Session middleware
------------------

.. module:: kay.sessions.middleware
   :synopsis: Session middleware.

.. class:: kay.sessions.middleware.SessionMiddleware

Enables session support. See the :doc:`session`.

Authentication middleware
-------------------------

.. module:: kay.auth.middleware
  :synopsis: Authentication middleware.

.. class:: kay.auth.middleware.AuthenticationMiddleware

Adds the ``user`` attribute, representing the currently-logged-in user, to
every incoming ``Request`` object. See :doc:`auth`.

