===============
Kay URL Mapping
===============

Overview
--------

For now, kay has one global url mapping and one global
endpoint-to-view dictionary per project unless you use SUBMOUNT_APP
feature. Kay automatically collects all the url rules and
endpoint-to-view dictionaries from installed applications(according to
the settings in the file settings.py), and put them into the global
ones.

How does it work?
-----------------

A newly created application by ``manage.py startapp`` command already
has a default ``urls.py`` in it. The ``urls.py`` has a function named
``make_rules``, which should return an instance of RuleFactory or
Rule.

Kay just detects and import ``appname.urls`` module, and merge this
RuleFactory into the global one.

This Rules will be mounted on the url ``/appname`` by default, you can
customize the mount point by adding ``{'appname': '/mount_path'}``
style entry to the ``APP_MOUNT_POINTS`` variable.

The default ``urls.py`` has a module level global dictionary named
``all_views`` as well. Kay will detects these dictionaries and update
the global one with these dictionaries automatically.

Adding your view
----------------

To add your original view, you need to edit ``urls.py`` in your
application directory. Let's say we have our application named
``myapp``, and we want to add our original view. The default
``urls.py`` has a ``index`` view bound to the url ``/myapp/``. Here is
the default ``urls.py``.

.. code-block:: python

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

For the details of how to configure the url mappings, perhaps you can
check werkzeug's manual hosted at following URL:

  http://werkzeug.pocoo.org/documentation/
