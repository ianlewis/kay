=========
Debugging
=========

Werkzeug debugger
=================

Kay has werkzeug's debugger integrated in it, and it is enabled in
local dev environment by default. Unfortunately, it can not be used on
appengine server environment.

This debugger works on developer's web browser, and it will run when
catching any exception. You can use an interactive console and
view-source capability on each step of the tracebacks when the
exception occurs.

Also, you can view tracebacks in a plain text format, and post these
tracebacks to a paste service hosted on the internet.


Debugger display
----------------

When an exception raises on dev environment, you can get following
display:

.. image:: images/debugger.png
   :scale: 80

Lineno and source code of each step of tracebacks are
displayed. Following icons are showed in the right side of the row
when you put your mouse cursor onto the rows of source code.

.. image:: images/debugger-icons.png

If you click on the left icon, an interactive console will be
displayed. If you click on the right iocn, you can view source code
with the problematic line highlighted.


Interactive console
-------------------

Here is a screenshot of an interactive console.

.. image:: images/debugger-console-startup.png
   :scale: 80

In this console, you can execute any python code with the frame
information at the time when the exception occurs, so its very helpful
for debugging.

For example, execute ``locals()``, you can get the dictionary for
local variables.

.. code-block:: python

  [console ready]
  >>> locals()
  {'request': <Request 'http://localhost:8080/' [GET]>}
  >>>

Fixing TYPO and re-executing your code will give you the correct result.

.. code-block:: python

  [console ready]
  >>> comments = Comment.all().order('-created').fetch(100)
  >>> comments
  [<myapp.models.Comment object at 0x104c6c8d0>]
  >>> 

If you click the console icon again, you can hide the interactive console.


View source
-----------

Here is the souce code view. You can see the problematic line is highlighted.

.. image:: images/debugger-view-source.png
   :scale: 80

If you click on the title that shows ``View Source``, you can hide the source code view.


View traceback as plaintext 
----------------------------

If you want to paste the traceback onto e-mail or something like that,
you can click on the title that shows ``Traceback`` as bellow.

.. image:: images/debugger-traceback-title.png
   :scale: 80

If you click on this title, the way for displaying traceback will be
changed into Debugger/Plaintext in turn. Here is the display for
viewing traceback in Plaintext.

.. image:: images/debugger-plaintext-view.png
   :scale: 80

Post your traceback
-------------------

When you view your traceback as Plaintext, there is a button with a
text ``create paste``. If you click on this button, Kay will post your
traceback to a paste service hosted at: http://paste.shehas.net/. If
the post succeeds, a link for that paste will be shown.

.. image:: images/debugger-paste-succeed.png
   :scale: 80

Here is a screenshot of the paste service.

.. image:: images/debugger-paste-service.png
   :scale: 80

Exception in Jinja2 template
----------------------------

If an exception occurs in Jinja2 template, you will see wired
traceback on the debugger. That is because of the restriction of
appengine( can not use ctypes). For a workaround, we can patch
dev_appserver.py in appengine SDK.

After adding 'gestalt' and '_ctypes' to the list
``_WHITE_LIST_C_MODULES``, you can see normal tracebacks on the
debugger.

Having said that, some python distribution has a broken ctypes(ex:
recent python25 in macports), and above workaround won't work with
broken ctypes. In such a case, copying _speedups.so into the directory
``kay/lib/jinja2`` from another jinja2 installation(not from bundled
in Kay), and adding '_speedups' to the list ``_WHITE_LIST_C_MODULES``
could be another workaround. If you're using MacOSX, the easiest way
to get compiled _speedups.so is to install py25-jinja2 with macports.


Using pdb
=========

You can also use pdb for debugging in dev environment. If you invoke
:func:`kay.utils.set_trace` anywhere on your code, the execution of
your program will stop. You can see a pdb prompt on the console in
which you invoked ``manage.py runserver``.

For example, you can execute your program step by step with a command
``step``. For more details how to use pdb, please refer to following
URL:

* http://www.python.org/doc/2.5.4/lib/debugger-commands.html
