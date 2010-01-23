.. module:: settings

====================
Settings Config File
====================

This is a list of available settings that can be modified
to customize the behavior of your application.


Items
=====

.. attribute:: APP_NAME

   The application name. The default is ``kay_main``.

   
.. attribute:: DEFAULT_TIMEZONE

   The default local timezone in string, e.g: 'Asia/Tokyo'. The default is ``Asia/Tokyo``. If it's not specified Kay automatically set ``UTC``. You can get the valid TimeZone list by reffering to ``kay/lib/pytz/all_timezone``.


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

   If set to ``True``, a profiling information will be displayed on the
   browser following normal application's response. The default is ``False``.


.. attribute:: PRINNT_CALLERS_ON_PROFILING

   If set to ``True``, callers will displayed on the browser with profiling information. The default is ``False``. 

   
.. attribute:: PRINNT_CALLEES_ON_PROFILING

   If set to ``True``, callees will displayed on the browser with profiling information. The default is ``False``. 

   
.. attribute:: SECRET_KEY

   The seed to generate a hash value. The default is ``ReplaceItWithSecretString``. Please be sure to rewrite this.


.. attribute:: SESSION_PREFIX

   The prefix of session name. The default is ``gaesess:``.

   
.. attribute:: COOKIE_AGE

   The cookie's age. The default is ``1209600`` seconds (2 weeks).

   
.. attribute:: COOKIE_NAME

   The cookie's name. The default is ``KAY_SESSION``.

   
.. attribute:: SESSION_MEMCACHE_AGE

   The session information's age. The default is ``3600`` seconds (1 hour).

   
.. attribute:: LANG_COOKIE_NAME

   The cookie's name for the language. The default is ``hl``.
   If i18n is enabled, Kay will display pages in the language specified with this cookie.
   Otherwise Kay identifies the language from Accept-Language setting of the browser.

   
.. attribute:: CACHE_MIDDLEWARE_SECONDS

   Specify how long to remain caches of HTML responses that views returned.
   The default is ``3600`` (1 hour).

   
.. attribute:: CACHE_MIDDLEWARE_NAMESPACE

   The namespace of HTML response cache. The default is ``CACHE_MIDDLEWARE``.
   
   
.. attribute:: CACHE_MIDDLEWARE_ANONYMOUS_ONLY

   If set to ``True``, HTML response cache will remain only while user login. The default is ``True``.

   
.. attribute:: ADD_APP_PREFIX_TO_KIND

   If set to ``True``, you can add an application prefix to ``db.Model.kind()`` method.
   The value of ``kind()`` will set to be ``applicationname_modelname`` (uncapitalized).

.. attribute:: FORMS_USE_XHTML

   If set to ``True``, :mod:`kay.utils.forms` renders forms in an
   xhtml comliant manner. The default is ``False``.
   
.. attribute:: ROOT_URL_MODULE

   You can have another URL settings file other than ``urls.py`` of each application.
   Specify the URL file's module name here. The default is ``urls``.

   
.. attribute:: MEDIA_URL

   The path to media files. The defautl is ``/media``.

   
.. attribute:: INTERNAL_MEDIA_URL

   The path to media files directory that bundle applications (e.g. ``kay.auto`` ) use.
   The default is ``/_media``.
   
   
.. attribute:: ADMINS

   Specify the administrator's username and email address in this tuple.
   If some exception occurs on the server, Kay send the traceback to this email address.
   This function works when you disable Debug ( ``DEBUG=False`` ).

   (setting example)

   .. code-block:: python

      ADMINS = (
        ('John', 'john@example.com'),
        ('Mary', 'mary@example.com')
      )

	  
.. attribute:: TEMPLATE_DIRS

   Allows you to specify the directory where Kay will look for your
   templates. This is a list of relative paths from your project root
   to your template directories.


.. attribute:: USE_I18N

   If set to ``True``, i18n works. The default is ``True``.

   .. seealso:: :doc:`i18n`

   
.. attribute:: INSTALLED_APPS

   This tupple must contain application names you want to
   activate. Default value is an empty tupple.


.. attribute:: APP_MOUNT_POINTS

   Specify the URL path to access each application in this dictionary.
   The key is the applicaion and the value is the URL path.
   If not specified, the URL path will be set ``/application's module name`` by default.

   .. code-block:: python

     APP_MOUNT_POINTS = {
       'bbs': '/',
       'categories': '/c',
     }

   
.. attribute:: CONTEXT_PROCESSORS

   Specify the path of context processors in this tuple. If you add
   context proccssors, you can add context variables which the jinja2
   template engine use in its rendering process. The default is an
   empty tuple.

   Here are examples:

   .. code-block:: python

      CONTEXT_PROCESSORS = (
        'kay.context_processors.request',
        'kay.context_processors.url_functions',
        'kay.context_processors.media_url',
      )
  

.. attribute:: JINJA2_FILTERS

   A dictionary of filter name to callable filters that are automatically
   loaded into the Jinja2 environment.

	  
.. attribute:: JINJA2_ENVIRONMENT_KWARGS

   The keyword arguments passed to Jinja2 contructor. The default is following.

   .. code-block:: python

      JINJA2_ENVIRONMENT_KWARGS = {
        'autoescape': True,
      }

	
.. attribute:: JINJA2_EXTENSIONS

   A list of Jinja2 extension classes. These are automatically
   imported and loaded into the Jinja2 environment.


.. attribute:: SUBMOUNT_APPS

   If you'd like to run applications with entirely-differnt settings,
   you can set them here. The default is an empty tuple.
   
.. attribute:: MIDDLEWARE_CLASSES

   Specify additional middlewares to this tuple. The default is an
   empty tuple. Here are examples:

   .. code-block:: python

     MIDDLEWARE_CLASSES = (
       'kay.session.middleware.SessionMiddleware',
       'kay.auth.middleware.AuthenticationMiddleware',
     )

	  
.. attribute:: AUTH_USER_BACKEND

   The backend class for user authentication. The default is ``kay.auth.backends.googleaccount.GoogleBackend``.
   
   .. seealso:: :doc:`auth`

   
.. attribute:: AUTH_USER_MODEL

   The model class for saving the user data authenticated by the backend.
   When you use the user class inherites from ``GoogleUser`` for authentication,
   you have to set it here. The defautl is ``kay.auth.models.GoogleUser``.

   .. seealso:: :doc:`auth`

   
.. attribute:: USE_DB_HOOK

   If set to ``True``, DB hook is enabled. DB hook is similar to Django's signal.
   You can run some processes when datastore is accessed.
   If you are unfamiliar with DB hook, you should set this to ``False``.
   The default is ``False``.
