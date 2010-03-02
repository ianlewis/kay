===========
View の定義
===========

概要
====

``views.py`` は、ビジネスロジックを書くために必要なモジュールです。view は呼び出し可能であること、第１引数にリクエストオブジェクトをとること、 :class:`werkzeug.Response` のインスタンスを返すこと、を満たす必要があります。



いちばん簡単な view
-------------------

いちばん簡単な view を見てみましょう。

myapp/views.py:

.. code-block:: python

  # -*- coding: utf-8 -*-
  # The simplest view. 

  from werkzeug import Response
  def index(request):
    return Response("Hello")

超簡単ですね。ページのレンダリングに html テンプレートを使いたい場合は :func:`kay.utils.render_to_response` を使ってください。

myapp/views.py:

.. code-block:: python

  # -*- coding: utf-8 -*-
  # The simplest view. 

  from werkzeug import Response
  from kay.utils import render_to_response

  def index(request):
    return render_to_response('myapp/index.html', {'message': 'Hello'})

これだけです。詳しくは :func:`kay.utils.render_to_response` を参照してください。


クラスベースの view
-------------------

view には呼び出し可能なオブジェクトを使うことができます。これは、 :class:`kay.handlers.BaseHandler` を拡張し、自分でハンドラクラスを定義することによって可能になります。

簡単なクラスベースの view の例を示します。

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

このハンドラは HTTP メソッドを小文字で書いたのと同名のメソッドをひとつ以上持っていなければなりません。また、現在の HTTP リクエストが使っている HTTP メソッドを実行する前に何らかの処理をさせるために、 ``perpare`` メソッドをもたせることができます。
