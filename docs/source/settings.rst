.. module:: settings

====================
settings config file
====================

You can configure settings config file for customizing Kay
application's behavior.


.. attribute:: INSTALLED_APPS

   This tupple must contain application names you want to
   activate. Default value is an empty tupple.


.. attribute:: DEFAULT_TIMEZONE

   Specify the default local timezone in string, e.g: 'Asia/Tokyo'


.. attribute:: DEBUG

   This attribute has different effect on local dev server and
   appengine server.

   * Local environment:

     If DEBUG is set to True, werkzeug's debugger will come up on any
     uncaught exception. Otherwise, it just displays 500 error, and
     tracebacks will be printed on console.

   * Server environment:

     If DEBUG is set to True, it displays tracebacks on your browser
     on any uncaught exception. Otherwise, it displays a simple error
     message to end users, and tracebacks will be sent to
     administrators by email.

.. attribute:: PROFILE

   If set to True, a profiling information will be displayed on the
   browser following normal application's response.

