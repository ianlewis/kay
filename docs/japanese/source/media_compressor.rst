
======================
Using media compressor
======================

.. note::

   This feature is still under Beta status. Implementations may change
   in the future.

Overview
========

If your application has lots of javascript and css files, it will take
some costs for loading all of these files. You can use ``media
compressor`` in this case for reducing page-loading costs.

By default, Kay uses bundled jsmin module for compressing javascripts,
and uses concatinating algorithms(literally, just concatinating all
the css files) for css files.

You can change what tool to use for compressing javascript files and
css files independently.

Compressed files are stored in ``_generated_media`` directory by
default. You need to add this directory to your static file
configuration in app.yaml.

Media compressor quick start
============================

To use media compressor, you need to add one jinja2 extension to
xJINJA2_EXTENSIONS variable, and add two configuratoin variables.

Let's say you have following media directory:

.. code-block:: bash

   $ tree media
   media
   |-- css
   |   |-- base_layout.css
   |   |-- common.css
   |   |-- component.css
   |   |-- fonts.css
   |   |-- subpages.css
   |   `-- toppage.css
   |-- images
   `-- js
       |-- base.js
       |-- jquery-ui.min.js
       |-- jquery.min.js
       |-- subpage.js
       `-- toppage.js

In your toppage, you're using jquery stuff, base.js, toppage.js, and all the css files except for subpages.css. In your subpage, you're using base.js, subpage.js, and all the css files except for toppage.css.

Here are simple configurations for this situation:

settings.py:

.. code-block:: python

   JINJA2_EXTENSIONS = (
     'jinja2.ext.i18n',
     'kay.ext.media_compressor.jinja2ext.compress',
   )

   COMPILE_MEDIA_JS = {
     'toppage.js': {
       'output_filename': 'toppage.js',
       'source_files': (
	 'media/js/jquery.min.js',
	 'media/js/jquery-ui.min.js',
	 'media/js/base.js',
	 'media/js/toppage.js',
       ),
     },
     'subpages.js': {
       'output_filename': 'subpages.js',
       'source_files': (
	 'media/js/base.js',
	 'media/js/subpage.js',
       ),
     },
   }

   COMPILE_MEDIA_CSS = {
     'toppage.css': {
       'output_filename': 'toppage.css',
       'source_files': (
	 'media/css/common.css',
	 'media/css/component.css',
	 'media/css/fonts.css',
	 'media/css/base_layout.css',
	 'media/css/toppage.css',
       ),
     },
     'subpages.css': {
       'output_filename': 'subpages.css',
       'source_files': (
	 'media/css/common.css',
	 'media/css/component.css',
	 'media/css/fonts.css',
	 'media/css/base_layout.css',
	 'media/css/subpages.css',
       ),
     },
   }

yourapp/templates/index.html:

.. code-block:: html

   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
   <html>
   <head>
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
   <title>Top Page</title>
   {% compiled_css('toppage.css') %}
   {% compiled_js('toppage.js') %}
   </head>
   <body>
   Your html goes here
   </body>
   </html>

In development server, compression is disabled by default, so these
compiled_*** tag will expanded just like following:

.. code-block:: html

   <link type="text/css" rel="stylesheet" href="/media/css/common.css" /> 
   <link type="text/css" rel="stylesheet" href="/media/css/component.css" /> 
   <link type="text/css" rel="stylesheet" href="/media/css/fonts.css" /> 
   <link type="text/css" rel="stylesheet" href="/media/css/base_layout.css" /> 
   <link type="text/css" rel="stylesheet" href="/media/css/toppage.css" /> 

   <script type="text/javascript" src="media/js/jquery.min.js"></script> 
   <script type="text/javascript" src="media/js/jquery-ui.min.js"></script> 
   <script type="text/javascript" src="media/js/base.js"></script> 
   <script type="text/javascript" src="media/js/toppage.js"></script> 


To compile these files, you need to invoke ``compile_media``
subcommand with ``manage.py`` script.

.. code-block:: bash

   $ python manage.py compile_media
   Running on Kay-0.8.0
   Compiling css media [toppage.css]
    concat /Users/tmatsuo/work/mediatest/media/css/common.css
    concat /Users/tmatsuo/work/mediatest/media/css/component.css
    concat /Users/tmatsuo/work/mediatest/media/css/fonts.css
    concat /Users/tmatsuo/work/mediatest/media/css/base_layout.css
    concat /Users/tmatsuo/work/mediatest/media/css/toppage.css
   Compiling css media [subpages.css]
    concat /Users/tmatsuo/work/mediatest/media/css/common.css
    concat /Users/tmatsuo/work/mediatest/media/css/component.css
    concat /Users/tmatsuo/work/mediatest/media/css/fonts.css
    concat /Users/tmatsuo/work/mediatest/media/css/base_layout.css
    concat /Users/tmatsuo/work/mediatest/media/css/subpages.css
   Compiling js media [toppage.js]
   Compiling js media [subpages.js]

   $ tree _generated_media

   _generated_media
   `-- 1
       |-- css
       |   |-- subpages.css
       |   `-- toppage.css
       `-- js
	   |-- subpages.js
	   `-- toppage.js

   3 directories, 4 files

To enable serving these files from this directory, you may need to add
the directory to app.yaml file (according to the version of Kay you're
using, you don't need to this) as follows:

.. code-block:: yaml

   - url: /_generated_media
     static_dir: _generated_media

Now, you can deploy your application to the appspot with compressed
media. In this case, actual rendered html top page looks like follows:

.. code-block:: html

   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> 
   <html> 
   <head> 
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> 
   <title>Top Page - myapp</title> 
   <link type="text/css" rel="stylesheet" href="/_generated_media/1/css/toppage.css" /> 

   <script type="text/javascript" src="/_generated_media/1/js/toppage.js"></script> 

   </head> 
   <body> 
   Your contents go here.
   </body> 
   </html>

References
==========

Available tool options for javascript files are:

* ``concat``

  Just concatinating all the javascripts

* ``jsminify``

  Use bundled jsmin module for compressing javascripts

* ``goog_calcdeps``

  Use calcdeps.py in google's closure library for
  compressing/calclating dependencies.

Available tool options for css files are:

* ``separate``

  Just copying all the css files

* ``concat``

  Just concatinating all the css files

* ``csstidy``

  Use csstidy for compressing css files. You need to install csstidy
  by yourself.


TODO
====

* Image handling
* More detailed references


