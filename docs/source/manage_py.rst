=================
Management script
=================

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

.. program:: manage.py add_translations

add_translations action
-----------------------

This action adds a new language catalogue for specified application.

.. code-block:: bash

  $ python manage.py add_translation [options]

.. cmdoption:: -a <app_name>

   Specify target app_name.

.. cmdoption:: -l <lang>

   Specify language code, e.g) ja/en/fr

.. cmdoption:: -f

   If specified, any existing catalogue will be overwritten.


.. _appcfg_label:

manage.py appcfg
----------------

This action is in charge of doing some tasks which appcfg.py does in a
pure GAE environment.  Here's a usage of appcfg action:

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

Current version of Kay loads only preparsed jinja2 templates in GAE
environment, so you have to preparse all of your jinja2 template files
before deploying your application. The ``manage.py`` script
automatically do this job, so you don't have to worry about it
usually. If you use launcher on MacOSX, please keep in mind that just
push ``deploy`` button on it won't care about preparsing jinja2
templates. In such a case, for preparsing jinja2 templates, you can
execute :ref:`preparse_apps`.


.. program:: manage.py bulkloader

manage.py bulkloader
--------------------

Execute bulkloader script with appropriate parameters.
For more details, please invoke 'python manage.py bulkloader --help'.

.. code-block:: bash

  $ python manage.py bulkloader [option]

.. cmdoption:: --help

   show help.

.. seealso:: http://code.google.com/intl/ja/appengine/docs/python/tools/uploadingdata.html


.. program:: manage.py clear_datastore

manage.py clear_datastore
-------------------------

Clear all data on appengine using remote APIs.

.. code-block:: bash

  $ python manage.py clear_datastore

.. cmdoption:: -a <appid>, --appid <appid>

   Specify the target application by ``app-id``. By default this command uses the value of ``application`` in ``app.yaml``.

.. cmdoption:: -h <host>, --host <host>

   Specify the target application by host. The default is ``app-id.appspot.com``.

.. cmdoption:: -p <path>, --path <path>

   The path to the remote APIs. The default is ``/remote_api``.

.. cmdoption:: -k <kinds>, --kinds <kinds>

   Specify the Kind of entity you want to clear. The Kind is ``appname_model`` by default. If not specified all models are targeted.

.. cmdoption:: -c, --clear-memcache

   Clear all data on memcache.

.. cmdoption:: --no-secure

   Use HTTP instead of HTTPS to communicate with App Engine.


.. seealso:: :doc:`dump_restore`



.. program:: manage.py compile_translations

manage.py compile_translations
------------------------------

Compile all i18n cagalog files of the application.

.. code-block:: bash

  $ python manage.py compile_translations

.. cmdoption:: -t <target>, --target <target>

   Specify the targeted directory.

.. cmdoption:: -a, --all

   Target all application.


   
.. program:: manage.py create_user

manage.py create_user
---------------------

Create a new user with remote APIs.

.. code-block:: bash

  $ python manage.py create_user

.. cmdoption:: -u <username>, --user-name <username>

   Specify the username.

.. cmdoption:: -P <password>, --password <password>

   Specify the password.

.. cmdoption:: -A, --is-admin

   Give user administrative privileges.

.. cmdoption:: -a <app-id>, --appid <app-id>

   Specify the target application by ``app-id``. By default this command uses the value of ``application`` in ``app.yaml``.

.. cmdoption:: -h <host>, --host <host>

   Specify the target application by host. The default is ``app-id.appspot.com``.

.. cmdoption:: -p <path>, --path <path>

   Specify the path to the remote APIs. The default is ``/remote_api``.

.. cmdoption:: --no-secure

   Use HTTP instead of HTTPS to communicate with App Engine.



.. program:: manage.py dump_all

manage.py dump_all
------------------

Dump all data from the server.

.. cmdoption:: --help

   Display help.

.. cmdoption:: -n <name>, --data-set-name <datasetname>

   Specfy the directory to save logfile and data. The command will make the diretory under ``_backup/``.

.. cmdoption:: -i <app-id>, --app-id <app-id>

   Specify the target application by ``app-id``.

.. cmdoption:: -u <url>, --url <url>

   Specify the target application by url.

.. cmdoption:: -d <diretory>, --directory <directory>

   Specify the diretory to dump data.

.. seealso:: :doc:`dump_restore`



.. program:: manage.py extract_messages

manage.py extract_messages
--------------------------

Extract the messages for i18n and create pot file.

.. code-block:: bash

  $ python manage.py extract_messages [options]

.. cmdoption:: -t <target>, --target <target>

   The target diretory.

.. cmdoption:: -a, --all

   Target all applications.

.. cmdoption:: -d <domain>, --domain <domain>

   * If set to ``messages``, the target files are Python script files and the template files in the ``templates`` diretory.
   * If set to ``jsmessages``, the target files are JavaScript files.
   

.. _preparse_apps:

manage.py preparse_apps
-----------------------

This commands execute preparsing all of your jinja2 templates
according to the values of your :attr:`settings.INSTALLED_APPS`.

.. code-block:: bash

  $ python manage.py preparse_apps


.. _preparse_bundle:

manage.py preparse_bundle
--------------------------

Preparse the Jinja2 templates in Kay itself. This command is for Kay developers.

.. code-block:: bash

   $ python manage.py preparse_bundle

  

.. program:: manage.py restore_all

manage.py restore_all
---------------------

Restore all data to the server.

.. code-block:: bash

   $ python manage.py restore_all [options]

.. cmdoption:: --help

   Display help.

.. cmdoption:: -n <datasetname>, --data-set-name <datasetname>

   Restore all data in the specified diretory in the ``_backup`` to the server.

.. cmdoption:: -i <appid>, --app-id <appid>

   Specify the target application by its ``appid``.

.. cmdoption:: -u <url>, --url <url>

   Specify the target application by its url.

.. cmdoption:: -d <directory>, --directory <directory>

   The diretory that data for restoring exists.

.. seealso:: :doc:`dump_restore`



.. program:: manage.py rshell

manage.py rshell
----------------

Start a new interactive python session with RemoteDatastore stub.

.. code-block:: bash

   $ python manage.py rshell [options]


.. cmdoption:: -a <appid>, --appid <appid>

   Specify the target application by its ``appid``

.. cmdoption:: -h <host>, --host <host>

   Specify the target application by its host. The default is ``appid.appspot.com``.

.. cmdoption:: -p <path>, --path <path>

   The path to the remote APIs. The default is ``/remote_api``.

.. cmdoption:: --no-useful-imports

   Run without automatic imports. If present, the command doesn't import application's model difinitions.

.. cmdoption:: --no-secure

   Use HTTP instead of HTTPS to communicate with App Engine.

.. cmdoption:: --no-use-ipython

   Start a not iPython session but a standard interactive python session.



.. program:: manage.py runserver

manage.py runserver
-------------------

Execute dev_appserver with appropriate parameters. For more details,
please invoke 'python manage.py runserver --help'.

.. code-block:: bash

   $ python manage.py runserver [options]

.. cmdoption:: --help

   Display help.

.. seealso:: http://code.google.com/intl/ja/appengine/docs/python/tools/devserver.html#The_Development_Console



.. program:: manage.py shell

manage.py shell
---------------

Start a new interactive python session.

.. code-block:: bash

   $ python manage.py shell [options]

  
.. cmdoption:: --datastore-path <path>

   The path to the datastore.

.. cmdoption:: --history-path <path>

   The path to the hisotry file of queries.

.. cmdoption:: --no-useful-imports

   Run without automatic imports. If present, the command doesn't import application's model difinitions.

.. cmdoption:: --no-use-ipython
   
   Start a not iPython session but a standard interactive python session.
    
.. seealso:: http://code.google.com/intl/ja/appengine/docs/python/tools/devserver.html#The_Development_Console



.. program:: manage.py startapp

manage.py startapp
------------------

Create a new application.

.. code-block:: bash

   $ python manage.py startapp myapp

  
  
.. program:: manage.py startproject

manage.py startproject
----------------------

Create a new project.

.. code-block:: bash

   $ python manage.py startproject myproject

.. cmdoption:: --proj-name projectname

   Specify the project name.


   
.. program:: manage.py test

manage.py test
--------------

Run test for installed applications.

.. code-block:: bash

   $ python manage.py test [options]

.. cmdoption:: --target APP_DIR

   Specify the target application diretory.

.. cmdoption:: -v <verbosity>, --verbosity <verbosity>

   Specify the log level of progression with integer. The default is ``0``.

   * ``0``: Nothing displayed
   * ``1``: Display the degree of progression with ``.``.
   * ``2``: Display the docstrings of test methods.


.. program:: manage.py update_translations

manage.py update_translations
-----------------------------

Update translation files using pot file.

.. code-block:: bash

   $ python manage.py update_translations [options]

.. cmdoption:: -t <target>, --target <target>

   Specify the targeted directory.

.. cmdoption:: -a

   Target all application.

.. cmdoption:: -l <lang>, --lang <lang>

   Specify the language to translate e.g.) -l ja

.. cmdoption:: -s, --statistics

   Display progree toward completion of translation.


