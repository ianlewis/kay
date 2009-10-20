===========
URL Mapping
===========

Overview
--------

Kay uses Werkzeug for mapping urls and for the request and response
objects passed to views.

For the full details about how to configure url mappings using Werkzeug,
please see Werkzeug's manual hosted at following URL:

  http://werkzeug.pocoo.org/documentation/0.5.1/routing.html

For now, kay has one global url mapping and one global
endpoint-to-view dictionary per project unless you use ``SUBMOUNT_APP``
feature. Kay automatically collects all the url rules and
endpoint-to-view dictionaries from installed applications(according to
the settings in the file settings.py), and put them into the global
ones.

How does it work?
-----------------

A newly created application created by the ``manage.py startapp`` command
already has a default ``urls.py`` in it. The ``urls.py`` has a function named
``make_rules``, which should return an instance of the ``Werkzeug`` ``RuleFactory``
or ``Rule`` class.

Kay automatically detects and imports the ``appname.urls`` module, and merges
the modules ``RuleFactory`` into the global one.

The imported Rules will be mounted on the url ``/appname`` by default, but you
can customize the mount point by adding an ``{'appname': '/mount_path'}``
style entry to the ``APP_MOUNT_POINTS`` variable in settings.py.

The default ``urls.py`` has a module level global dictionary named
``all_views`` as well. This is a dictionary containing endpoint name to 
view function mappings. The endpoint mappings here should match your 
endpoints specified in ``make_rules``. Kay will detect these dictionaries
and update the global one with these dictionaries automatically.

Adding your view
----------------

To add your custom view, you need to edit ``urls.py`` in your
application directory. Let's say we have our application named
``myapp``, and we want to add our original view. The default
``urls.py`` has a ``index`` view bound to the url ``/myapp/``. Here is
the default ``urls.py``.

.. code-block:: python

  from werkzeug.routing import EndpointPrefix, Rule

  def make_rules():
    return [
      EndpointPrefix('myapp/', [
	Rule('/', endpoint='index'),
      ]),
    ]

  all_views = {
    'myapp/index': myapp.views.index,
  }

Here is an example which adds ``index2`` view bound to the url
``/myapp/index2``:

.. code-block:: python

  from werkzeug.routing import EndpointPrefix, Rule

  def make_rules():
    return [
      EndpointPrefix('myapp/', [
	Rule('/', endpoint='index'),
	Rule('/index2', endpoint='index2'),
      ]),
    ]

  all_views = {
    'myapp/index': myapp.views.index,
    'myapp/index2': myapp.views.index2,
  }
