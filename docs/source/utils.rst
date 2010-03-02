=================
Utility functions
=================

.. module:: kay.utils

There are various useful functions in :mod:`kay.utils`.

.. function:: set_trace()

   Set pdb's set_trace with appropriate configuration.

.. function:: raise_on_dev()

   Raises A RuntimeError only on development environment.

.. function:: get_timezone(tzname)

   Get the timezone.

   :param tzname: The name of a timezone.
   :return: datetime.tzinfo implementation

.. function:: url_for(endpoint, **args)

   Get the URL to an endpoint. There are some special keyword arguments:

     `_anchor`: This string is used as URL anchor.

     `_external`: If set to `True` the URL will be generated with the full server name and `http://` prefix.

   :param args: Keyword arguments are used for building a URL
   :return: string representing the URL to an endpoint

.. function:: create_login_url(url=None)

   Get the URL for a login page.

   :param url: The URL which user is redirected after the login process. If none supplied, the current URL will be use.
   :return: string representing the login URL.   

.. function:: create_logout_url(url=None)

   Get the URL for a logout page.

   :param url: The URL which user is redirected after the logout process. If none supplied, the current URL will be use.
   :return: string representing the logout URL. 

.. function:: render_error(e)

   Render an instance of :class:`werkzeug.exceptions.HTTPException`
   with Jinja2 template.

   :param e: An instance of any subclass of :class:`werkzeug.exceptions.HTTPException`
   :return: An instance of :class:`werkzeug.Response`

.. function:: render_to_string(template, context={}, processors=None)

   A function for template rendering adding useful variables to context
   automatically, according to the CONTEXT_PROCESSORS settings.

   :param template: The pathname of a template.
   :param context: The context dictionary passed to the template.
   :param processors: The processors for ondemand use.
   :return: Rendered string

.. function:: render_to_response(template, context, mimetype='text/html', processors=None)

   A function for render html pages.

   :param template: The pathname of a template.
   :param context: The context dictionary passed to the template.
   :param processors: The processors for ondemand use.
   :param mimetype: The mimetype of :class:`werkzeug.Response`
   :return: Rendered response


.. function:: to_local_timezone(datetime, tzname=settings.DEFAULT_TIMEZONE)

   Convert a datetime object to the local timezone.
   
   :param datetime: datetime object with UTC timezone
   :param tzname: the name of a timezone
   :return: datetime.datetime object with new timezone

.. function:: to_utc(datetime, tzname=settings.DEFAULT_TIMEZONE)

   Convert a datetime object to UTC and drop tzinfo.

   :param datetime: datetime object with local timezone
   :param tzname: the name of a timezone
   :return: datetime.datetime object with UTC timezone

.. function:: get_by_key_name_or_404(model_class, key_name)

   Try to get the data with given key_name and return it or raise
   :class:`werkzeug.exceptions.NotFound` when failed.

   :param model_class: the model class
   :param key_name: the key_name passed to model_class.get_by_key_name
   :return: an instance of the model class on success

.. function:: get_by_id_or_404(model_class, id)

   Try to get the data with given id and return it or raise
   :class:`werkzeug.exceptions.NotFound` when failed.

   :param model_class: the model class
   :param id: the id passed to model_class.get_by_id
   :return: an instance of the model class on success

.. function:: get_or_404(model_class, key)

   Try to get the data with given key and return it or raise
   :class:`werkzeug.exceptions.NotFound` when failed.

   :param model_class: the model class
   :param id: the key passed to model_class.get
   :return: an instance of the model class on success
