===========
URL Mapping
===========

Overview
--------

Kay uses Werkzeug for mapping urls and your views.

For the full details about how to configure url mappings using Werkzeug,
please see Werkzeug's manual hosted at following URL:

  http://werkzeug.pocoo.org/documentation/0.6/routing.html

For now, kay has one global url mapping and one global
endpoint-to-view dictionary per project unless you use ``SUBMOUNT_APP``
feature. Kay automatically collects all the url rules and
endpoint-to-view dictionaries from installed applications(according to
the settings in the file settings.py), and put them into the global
ones.

How does it work?
-----------------

A newly created application created by the :command:`manage.py startapp` command
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

  import myapp.views

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

  import myapp.views

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

In above examples, we defined views with view callables. To do this,
we need to import our ``views`` module in urls module. Thus, this
could cause huge startup costs if your ``views`` module is very big or
you have many apps in your project. We can define these views as
string to avoid these costs. It allows Kay to load our views in lazily
manners.

Here is the re-written version of the last example defining views as
strings. Don't forget to remove ``import myapp.views`` statement for
this to work efficiently.

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
    'myapp/index': 'myapp.views.index',
    'myapp/index2': 'myapp.views.index2',
  }

Sometimes you may define class based views. How can you set those
class based view in your urlmapping in lazily manners? You can do this
as follows:

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
    'myapp/index': 'myapp.views.index',
    'myapp/index2': ('myapp.views.MyClassBasedView', (),
                     {"template_name": "myapp/mytemplate.html"}),
  }

In this example, an instance of ``MyClassBasedView`` will be created
on demand in the equivalent way as follows:

.. code-block:: python

   from myapp.views import MyClassBasedView
   view_func = MyClassBasedView(template_name="myapp/mytemplate.html")

.. seealso:: :doc:`views`


How to pass argments to your view
---------------------------------

You can add variable parts to a URL by marking these sections as
``<variable_name>``. These parts are passed as keyword argments to
your views. Here are some examples:

.. code-block:: python

  from werkzeug.routing import EndpointPrefix, Rule

  def make_rules():
    return [
      EndpointPrefix('myapp/', [
	Rule('/', endpoint='index'),
	Rule('/user/<username>', endpoint='user'),
	Rule('/post/<int:post_id>', endpoint='post')
      ]),
    ]

  all_views = {
    'myapp/index': 'myapp.views.index',
    'myapp/user': 'myapp.views.show_user_profile',
    'myapp/post': 'myapp.views.show_post',
  }


You need to write your views to accept these variables as follows:

.. code-block:: python

  # -*- coding: utf-8 -*-

  from werkzeug import Response
  from kay.utils import render_to_response

  # ..

  def show_user_profile(request, username):
    # ..
    # ..

  def show_post(request, post_id)
    # ..
    # ..


Introducing a new interface for urlmapping
------------------------------------------

.. Note::

  This interface is still under experimental stage, so detailed
  implementation/usage might change in the future.

In the new urlmapping system, you need to define ``view_groups``
global variable in your urls.py. The value must be a list or tuple of
ViewGroup instances.

``ViewGroup`` is a class which holds url rules and endpoint-view
mappings as its instance attributes. You can pass unlimited number of
``Rule`` instances to a constructor method of this class.

A constructor of ``Rule`` class accepts not only all the arguments
suitable for ``werkzeug.routing.Rule`` class's constructor but also
accepts ``view`` keyword argument.

Let's see the simplest example.

urls.py:

.. code-block:: python

  from kay.routing import (
    ViewGroup, Rule
  )

  view_groups = [
    ViewGroup(Rule('/', endpoint='index', view='myapp.views.index'))
  ]

By default, endpoint is prefixed with ``app_name/`` automatically, so
in this example, you need to pass 'myapp/index' to ``url_for()``
helper function.

To suppress this prefixing, you can just pass
``add_app_prefix_to_endpoint`` keyword argument with ``False`` value.
You can also define your own ViewGroup subclass and override
``add_app_prefix_to_endpoint`` class attribute to False:

Suppressing the prefix:

.. code-block:: python

  from kay.routing import (
    ViewGroup, Rule
  )

  view_groups = [
    ViewGroup(Rule('/', endpoint='index', view='myapp.views.index'),
              add_app_prefix_to_endpoint=False)
  ]


Please be aware an endpoint which is defined once will never be
overridden by following definition, because endpoint-view mapping is
just a dictionary.

If you need to define two or more Rules with the same endpoint, you
can omit redundant view keyword arguments in this case as follows:

.. code-block:: python

  view_groups = [
    ViewGroup(
      Rule('/list_entities', endpoint='index', view='myapp.views.index'),
      Rule('/list_entities/<cursor>', endpoint='index')
    )
  ]
