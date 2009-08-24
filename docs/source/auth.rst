====================
Using authentication
====================

Overview
--------

Google App Engine has a very nice default auth mechanism using google
account or google apps account. You can use this capability with
extensible manner with GoogleAuthenticationMiddleware. You can also
use username and password information stored in the app engine
datastore.

Helper functions and decorators
-------------------------------

There are helper functions in kay.utils module: create_logout_url and
create_login_url. These functions are automatically imported into
templates' rendering context. So you can use these functions in your
templates just like:

.. code-block:: html

  {% if request.user.is_anonymous() %}
    <a href="{{ create_login_url() }}">login</a>
  {% else %}
    Hello {{ request.user }}! <a href="{{ create_logout_url() }}">logout</a>
  {% endif %}

There are decorators in kay.auth.decorators module: login_required and
admin_required. You can decorate any view of yours with these
decorators just like:

.. code-block:: python

  @login_required
  def user_profile(request):
    """ This is a view for detailed information of the user's profile. 
    """
    ...
    ...
    
  @admin_required
  def manage_users(request):
    """ This is a view for user management.
    """
    ...
    ...

Using google account authentication
-----------------------------------

By default, kay.auth.middleware.GoogleAuthenticationMiddleware is
enabled. This middleware is for authentication using google account or
google apps account. If a user logs into your app first time, an
information of the user is stored as GoogleUser entity (It's just a
default setting, it is also customizable) in the GAE datastore. You
can use this middleware without using session capability.

To customize user model, you need to define new class extended from
kay.auth.models.GoogleUser, add any required properties to it, and set
the name of your new class to AUTH_USER_MODEL settings directive.

.. code-block:: python

  MIDDLEWARE_CLASSES = (
    'kay.auth.middleware.GoogleAuthenticationMiddleware',
  )
  AUTH_USER_MODEL = 'kay.auth.models.GoogleUser'


Using datastore authentication
------------------------------

To use this middleware, you need to set
'kay.auth.middleware.AuthenticationMiddleware' to MIDDLEWARE_CLASSES
settings directive, and also need to set
'kay.auth.models.DatastoreUser' (or a classname that is extended from
it) to AUTH_USER_MODEL settings directive. AuthenticationMiddleware
must be placed under SessionMiddleware that is mandatry for this
middleware.

.. code-block:: python

  MIDDLEWARE_CLASSES = (
    'kay.sessions.middleware.SessionMiddleware',
    'kay.auth.middleware.AuthenticationMiddleware',
  )
  AUTH_USER_MODEL = 'kay.auth.models.DatastoreUser'

For now, there is no any convenience method to create users into the
datastore. Please keep in mind that you need to set user's password in
a special hashed format. You can use kay.utils.crypto.gen_pwhash
function for this purpose. You also need to use key_name for a
performance reason. Here is the code to create new user in the
datastore.

.. code-block:: python

   from kay.utils.crypto import gen_pwhash
   from kay.auth.models import DatastoreUser

   user_name = 'newuser'
   password = 'newpassword'

   new_user = DatastoreUser(key_name=DatastoreUser.get_key_name(user_name),
                            user_name=user_name, password=gen_pwhash(password))
   new_user.put()

Using datastore authentication on an owned domain
-------------------------------------------------

TODO