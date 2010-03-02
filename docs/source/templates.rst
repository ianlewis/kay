=============
Using Jinja2 
=============

Overview
--------

Kay uses Jinja2 for rendering HTML templates. Kay does the legwork
of setting up the Jinja2 environment and loading extensions and filters.
As an added benefit Kay will also compile your templates down to
pure python code when deploying your application. This can boost
rendering speeds as the template doesn't need to be processesed
each time it is rendered.

Writing Templates
-----------------------

Writing templates is covered in depth by the `Jinja2 Template Designer Documentation <http://jinja.pocoo.org/2/documentation/templates>`_.

Context Processors
-----------------------

Much like Django's context processors Kay allows you to define a
number of functions that are run when templates are rendered that
make commonly used data available to your template.

A context processor is a python callable that takes a request
object and returns a dictionary object of data that is added
to the template context. The key in the dictionary is the
name given to the data in your template.

Each processor is applied in order. That means, if one processor
adds a variable to the context and a second processor adds a
variable with the same name, the second will override the first.
The default processors are explained below.

.. currentmodule:: kay.context_processors

.. function:: request()

Adds the ``Request`` object the the template context with the name request.

.. function:: url_functions()

This request context adds a number of useful url functions to the template
context (``url_for``, ``reverse``, ``create_login_url``, ``create_logout_url``)

.. function:: i18n()

This processor adds the current language_code to the template context
with the name langugage_code.

.. function:: media_url()

Adds the current :attr:`settings.MEDIA_URL` value to the template context with the name media_url.


Template Loading
--------------------------
You can tell Kay where your templates are located by using the :attr:`settings.TEMPLATE_DIRS` setting. This should be set to a list or tuple of strings that
contain relative paths from your project base directory to your template directory(ies). 
Example:

.. code-block:: python

  TEMPLATE_DIRS = (
    'templates/default',
    'templates/other',
  )

In this case Kay will look in the default directory first and if the template
does not exist there it will load the template from the other directory.

Extensions & Filters
--------------------------

Kay allows you to use Jinja2 extensions. You can set which Jinja2 extensions you
would like to use in :attr:`settings.JINJA2_EXTENSIONS`.
Filters are added the same way using the :attr:`settings.JINJA2_FILTERS` setting. However, the
``JINJA2_FILTERS`` setting is specified as a dictionary whose keys are the
names given to the added filters. Example:

.. code-block:: python

  JINJA2_EXTENSIONS = (
    'myapp.jinja2.extensions.my_extension',
  )

  JINJA2_FILTERS = {
    'my_filter': 'myapp.jinja2.filters.do_my_filter',
    'my_other_filter': 'my_other_app2.jinja2.filters.do_my_filter',
  }
