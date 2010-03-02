.. _wrappers:

==========================
Request / Response Objects
==========================

.. module:: werkzeug

Overview
========

Kay uses the request/response objects of Werkzeug which is WSGI-compliant. When accessed by browsers Kay creates request object and pass it to the view function specified by URL mapping. Views have to take the request object as the first argument, create an response object, and return it. In this chapter, we explain about the structure of request/response objects.


Request Object
==============

* Kay's Request Object is an instance of the :class:`Request` class of Werkzeug. 
* Views have to take the request object as the first argument.
* The request object is immutable. Modifications are not allowed.
* Per default the request object will assume all the text data is utf-8 encoded.


.. autoclass:: Request
   :members: accept_charsets, accept_encodings, accept_languages, accept_mimetypes, access_route, args, authorization, base_url, cache_control, content_length, content_type, cookies, data, date, encoding_errors, files, form, from_values, headers, host, host_url, if_match, if_modified_since, if_none_match, if_unmodified_since, is_behind_proxy, is_multiprocess, is_multithread, is_run_once, is_secure, is_xhr, max_content_length, max_form_memory_size, max_forwards, method, mimetype, mimetype_params, path, pragma, query_string, remote_addr, remote_user, script_root, stream, url, url_charset, url_root, user_agent, values
   :inherited-members:

   
   .. attribute:: environ

      The WSGI environment that the request object uses for data retrival.

   .. attribute:: shallow

      `True` if this request object is shallow (does not modify :attr:`environ`),
      `False` otherwise.

   .. attribute:: lang

	  Language that Kay estimated from the request.

   .. attribute:: user

   	  If authentication is enabled this is the user object specified in the ``AUTH_USER_MODEL`` of ``settings.py``

	  .. seealso:: :doc:`auth`

   .. attribute:: session

   	  If session is enabled this is the session data.

   	  .. seealso:: :doc:`session`

   .. attribute:: referrer

   	  Referrer.
	  
	  
Response Object
===============

* Kay's Response Object is an instance of the :class:`Response` class of Werkzeug. 


.. autoclass:: Response
   :members:
   :inherited-members:

   .. attribute:: response

      The application iterator.  If constructed from a string this will be a
      list, otherwise the object provided as application iterator.  (The first
      argument passed to :class:`BaseResponse`)

   .. attribute:: headers

      A :class:`Headers` object representing the response headers.

   .. attribute:: status_code

      The response status as integer.

   .. attribute:: direct_passthrough

      If ``direct_passthrough=True`` was passed to the response object or if
      this attribute was set to `True` before using the response object as
      WSGI application, the wrapped iterator is returned unchanged.  This
      makes it possible to pass a special `wsgi.file_wrapper` to the response
      object.  See :func:`wrap_file` for more details.

Throwing HTTP exceptions
------------------------

There are various exceptions in :mod:``werkzeug.exceptions``. Each
exception's name represents which type of HTTP Error. You can raise
these exceptions when you want return such errors to the users.

Here are the list of exceptions:

.. currentmodule:: werkzeug.exceptions

.. class:: HTTPException
.. class:: BadRequest
.. class:: Unauthorized
.. class:: Forbidden
.. class:: NotFound
.. class:: MethodNotAllowed
.. class:: NotAcceptable
.. class:: RequestTimeout
.. class:: Gone
.. class:: LengthRequired
.. class:: PreconditionFailed
.. class:: RequestEntityTooLarge
.. class:: RequestURITooLarge
.. class:: UnsupportedMediaType
.. class:: InternalServerError
.. class:: NotImplemented
.. class:: BadGateway
.. class:: ServiceUnavailable

	  
.. seealso:: http://werkzeug.pocoo.org/documentation/dev/wrappers.html
