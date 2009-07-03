=====================
Kay management script
=====================

Overview
--------

Kay has a management script named 'manage.py'. This script covers most
of the management tasks for your applications. Invoking it without any
parameters gives you help text.

Some of the tasks will invoking the commands provided by Google App
Engine SDK with little parameter adjustments, and some preparations
for the task.

So do not think about invoking such scripts(appcfg.py,
dev_appserver.py, bulkloader.py) directly from Google App Engine SDK.


Jinja2 preparsing
-----------------

Current version of Kay loads only preparsed jinja2 templates, so you
have to preparse before deploying your application. The manage.py
script automatically do this job, so you don't have to worry about it
usually. If you use launcher on MacOSX, please keep in mind that just
push 'deploy' button on it won't care about preparsing jinja2
templates. In such a case, to preparse jinja2 template, perhaps you
can execute following command:

.. code-block:: console

  $ python manage.py preparse_apps
