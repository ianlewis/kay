=====================
Kay management script
=====================

Overview
--------

Kay has a management script named ``manage.py``. This script covers
most of the management tasks for your applications. Invoking it
without any parameters gives you help text.

Some of the tasks will invoking the commands provided by Google App
Engine SDK with little parameter adjustments, and some preparations
for the task.

So do not think about invoking such scripts(appcfg.py,
dev_appserver.py, bulkloader.py) directly from Google App Engine SDK.

Appcfg subcommand
-----------------

This subcommand is in charge of doing some tasks which appcfg.py does
in a pure GAE environment.  Here's a usage of appcfg subcommand:

.. code-block:: bash

  $ python manage.py appcfg [options] <action>

Action must be one of:

 * cron_info: Display information about cron jobs.
 * download_data: Download entities from datastore.
 * help: Print help for a specific action.
 * request_logs: Write request logs in Apache common log format.
 * rollback: Rollback an in-progress update.
 * update: Create or update an app version.
 * update_cron: Update application cron definitions.
 * update_indexes: Update application indexes.
 * update_queues: Update application task queue definitions.
 * upload_data: Upload data records to datastore.
 * vacuum_indexes: Delete unused indexes from application.

``Help`` action followed by a particular action name will give you
help text for that action. So, for example, you'll get help texts for
``update`` action by typing as follows:

.. code-block:: bash

  $ python manage.py appcfg help update

Kay supplements argument with current directory automatically. So you
don't need to specify app's directory stated in action's ``help`` text
(Actually, it is a confusing behaviour, so it might be fixed in a
future version). For example, you can upload your application by just
typing as follows:

.. code-block:: bash

  $ python manage.py appcfg update  


Jinja2 preparsing
-----------------

Current version of Kay loads only preparsed jinja2 templates in GAE
environment, so you have to preparse before deploying your
application. The ``manage.py`` script automatically do this job, so
you don't have to worry about it usually. If you use launcher on
MacOSX, please keep in mind that just push ``deploy`` button on it
won't care about preparsing jinja2 templates. In such a case, to
preparse jinja2 template, perhaps you can execute following command:

.. code-block:: bash

  $ python manage.py preparse_apps


