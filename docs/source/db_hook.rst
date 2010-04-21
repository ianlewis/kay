=====================
Using db_hook feature
=====================

.. note::

   This feature is still under Beta status. Implementations may change
   in the future.

Overview
========

Appengine itself has a `RPC hook mechanism
<http://code.google.com/intl/en/appengine/articles/hooks.html>`_. However,
in this way, your hook functions just receive low-level
request/response objects, so its somewhat difficult to write such
functions for our purpose.

Kay has a feature for utilizing this hook mechanism more easily. The
package ``kay.utils.db_hook`` contains several functions for
registering your hook functions to the apiproxy hooks.

Functions
---------

.. module:: kay.utils.db_hook

.. function:: register_pre_save_hook(func, model)

   Register ``func`` to apiproxy's PreCallHooks indirectly. This
   function will be invoked only before an entity of specified model
   is saved.

.. function:: register_post_save_hook(func, model)

   Register ``func`` to apiproxy's PostCallHooks indirectly. This
   function will be invoked only after an entity of specified model is
   saved.

To these functions for registration, you can pass functions with
following signature:

.. code-block:: python

   def your_hook_function(entity, put_type_id):
     # do something with the entity
     # put_type_id is defined in kay.utils.db_hook.put_type

put_type_id indicates whether this entity is newly created or not by
guessing. put_type is defined in the module
``kay.utils.db_hook.put_type``.

.. code-block:: python

   NEWLY_CREATED = 1
   UPDATED = 2
   MAYBE_NEWLY_CREATED = 3
   MAYBE_UPDATED = 4
   UNKNOWN = 5

   type_names = {
     1: "Newly Created",
     2: "Updated",
     3: "Maybe Newly Created",
     4: "Maybe Updated",
     5: "Unknown",
   }

   def get_name(type):
     return type_names.get(type, None)

AFAIC, its impossible to detect perfectly whether an entity is going
to be newly created or just updated, only from low-level
request/response object without checking if there is stored entity
with the same key. So in this implementation, Kay just guess it by
checking created/updated timestamp of the entity.

You can check it in your pre save hook function by invoking
db.get(entity.key()) by yourself just like following:

.. code-block:: python

   # this code snippet shows how to write hooks for doing something
   # only before entity creation. You need to use pre save hook for
   # this purpose.

   import logging

   from google.appengine.ext import db
   from kay.utils.db_hook import register_pre_save_hook

   from myapp.models import comment

   def log_on_creation(entity,put_type_id):
     if db.get(entity.key()) is None:
       # this is an newly created entity
       logging.debug("Entity: %s is going to be created." % entity.key())

.. function:: register_pre_delete_hook(func, model)

   Register ``func`` to apiproxy's PreCallHooks indirectly. This
   function will be invoked before an entity of specified model is
   deleted.

To this delete hook, you can pass functions with following signature:

.. code-block:: python

   def your_hook_function(key):
     # do something with the key
