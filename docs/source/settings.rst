.. module:: settings

====================
Settings Config File
====================

This is a list of available settings that can be modified
to customize the behavior of your application.

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

.. attribute:: TEMPLATE_DIRS

   Allows you to specify the directory where Kay will look for your
   templates. This is a list of relative paths from your project root
   to your template directories.

.. attribute:: JINJA2_EXTENSIONS

   A list of Jinja2 extension classes. These are automatically
   imported and loaded into the Jinja2 environment.

.. attribute:: JINJA2_FILTERS

    A dictionary of filter name to callable filters that are automatically
    loaded into the Jinja2 environment.
