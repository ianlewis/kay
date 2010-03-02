===============
Defining views 
===============

Overview
========

``views.py`` is a module in which you need to write your business
logic. A single view must be callable, must have request object as a
first argument, and must return an instance of
:class:`werkzeug.Response`.

The simplest view
-----------------

Let's look at the simplest view.

myapp/views.py:

.. code-block:: python

  # -*- coding: utf-8 -*-
  # The simplest view. 

  from werkzeug import Response
  def index(request):
    return Response("Hello")

It's super easy. What if you want to use html templates for rendering
pages. Please use :func:`kay.utils.render_to_response` for this
purpose:

myapp/views.py:

.. code-block:: python

  # -*- coding: utf-8 -*-
  # The simplest view. 

  from werkzeug import Response
  from kay.utils import render_to_response

  def index(request):
    return render_to_response('myapp/index.html', {'message': 'Hello'})

That's it. Please see :func:`kay.utils.render_to_response` for more
details.

Class based views
-----------------

You can use callable object as a view. For this purpose, you can
extend :class:`kay.handlers.BaseHandler` and define your own handler
class.

Here is a example for a simple class based view:

.. code-block:: python

  from kay.handlers import BaseHandler

  from myapp.models import Comment

  # ..

  class CommentHandler(BaseHandler):
    def prepare(self):
      self.comments = Comment.all().order('-created').fetch(100)
      self.form = CommentForm()

    def get(self):
      return render_to_response('myapp/index.html',
			 	{ 'comments': self.comments,
				 'form': self.form.as_widget()})

    def post(self):
      if self.form.validate(self.request.form):
	if self.request.user.is_authenticated():
	  user = self.request.user
	else:
	  user = None
	new_comment = Comment(body=self.form['comment'],user=user)
	new_comment.put()
	return redirect(url_for('myapp/index'))
      return self.get()

  comment_handler = CommentHandler()

These handler must have one or more methods with a name as the same as
lower-cased HTTP Methods to corresponds with. It can have ``prepare``
method to do some task before above methods whatever HTTP method the
current HTTP request uses.