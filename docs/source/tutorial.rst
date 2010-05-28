============
Kay tutorial
============

Preparation
-----------

Install following stuff::

  * Python-2.5
  * App Engine SDK/Python
  * Kay Framework
  * ipython (recommended)

If you install python25 from macports, you also need to install following::

  * py25-hashlib
  * py25-socket-ssl
  * py25-pil
  * py25-ipython (recommended)

If you retreive Kay from the repository, you need to install mercurial::

  * mercurial

You can retreive source code of Kay as follows.

.. code-block:: bash

  $ hg clone https://kay-framework.googlecode.com/hg/ kay

If you use released stable version, you can download the latest
released tarball from
http://code.google.com/p/kay-framework/downloads/list and unpack it as
follows:

.. code-block:: bash

   $ tar zxvf kay-VERSION.tar.gz

.. Note::

   In this tutorial, we use Kay-0.10.0 or higher, so if Kay-0.10.0 has
   been released, you can use the release version, otherwise please
   use the code from Kay's repository.

If you have installed a zip version of appengine SDK, please create a
symbolic link as follows:

.. code-block:: bash

   $ sudo ln -s /some/whare/google_appengine /usr/local/google_appengine    

If you have used an installer of appengine SDK, you don't need to
create the symlink.

Quick start
-----------

Starting a new project
======================

To start a new project, you can use ``manage.py`` script offered by
Kay for creating a skelton of your project. After that, you're
supposed to use a newly created ``manage.py`` script in the project
directory for managing this project(including deployment, testing,
i18n translation work, etc, etc..).

.. code-block:: bash

   $ python kay/manage.py startproject myproject
   $ tree myproject
   myproject
   |-- app.yaml
   |-- kay -> /Users/tmatsuo/work/tmp/kay/kay
   |-- manage.py -> /Users/tmatsuo/work/tmp/kay/manage.py
   |-- settings.py
   `-- urls.py

   1 directory, 4 files

On platforms that supports symbolic link, two symbolic link for a
directory ``kay`` and a file ``manage.py`` are created.

Creating an application
=======================

With kay, you need to create at least one application in your project.

Change directory into the newly created ``myproject`` directory, and
create your first application. In an example bellow, an application
named ``myapp`` is created.

.. code-block:: bash

   $ cd myproject
   $ python manage.py startapp myapp
   $ tree myapp
   myapp
   |-- __init__.py
   |-- models.py
   |-- templates
   |   `-- index.html
   |-- urls.py
   `-- views.py

   1 directory, 5 files

After creating an application, you need to edit ``settings.py`` for
registering your application to the project.

First, please add ``myapp`` to a tuple ``settings.INSTALLED_APPS``. If
necessary, you can configure which URL to mount this application by
setting a dictionary ``APP_MOUNT_POINTS``. An example bellow shows how
to mount your application at a URL '/'.

settings.py

.. code-block:: python

  #$/usr/bin/python
  #..
  #..

  INSTALLED_APPS = (
    'kay.auth',
    'myapp',
  )

  APP_MOUNT_POINTS = {
    'myapp': '/',
  }

Unless setting ``APP_MOUNT_POINTS``, the application will be mounted
at a URL come from the application name like ``/myapp``. 

In the example above, as you see, we added another application named
``kay.auth`` for later use.

Running your application
========================

Let's run your first application. You can run the development server
by following command.

.. code-block:: bash

  $ python manage.py runserver
  INFO     2009-08-04 05:48:21,339 appengine_rpc.py:157] Server: appengine.google.com
  ...
  ...
  INFO     ... Running application myproject on port 8080: http://localhost:8080


You will see just 'Hello' on your browser by accessing
http://localhost:8080/.


Deployment
==========

Before looking into the code, let's deploy this project to
appspot. First, you need to edit ``app.yaml`` and set your ``appid``
as ``application``. After that, please do as follows.

.. code-block:: bash

  $ python manage.py appcfg update

In case you're asked for a username and password, please type in your
credentials here. After successful deployment, you can access your
application at http://your-appid.appspot.com/.


Quick look into a skelton
-------------------------

myapp/urls.py
=============

First, here is a default ``urls.py``. You can configure a mapping
between URLs and your views here.

myapp/urls.py:

.. code-block:: python

   from kay.routing import (
     ViewGroup, Rule
   )

   view_groups = [
     ViewGroup(
       Rule('/', endpoint='index', view='myapp.views.index'),
     )
   ]

In the ``Rule`` line, there is a mapping like '/' ->
'myapp.views.index'.

myapp/views.py
==============

Basically, you are supposed to write your logic here.

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   myapp.views
   """

   """
   import logging

   from google.appengine.api import users
   from google.appengine.api import memcache
   from werkzeug import (
     unescape, redirect, Response,
   )
   from werkzeug.exceptions import (
     NotFound, MethodNotAllowed, BadRequest
   )

   from kay.utils import (
     render_to_response, reverse,
     get_by_key_name_or_404, get_by_id_or_404,
     to_utc, to_local_timezone, url_for, raise_on_dev
   )
   from kay.i18n import gettext as _
   from kay.auth.decorators import login_required

   """

   from kay.utils import render_to_response


   # Create your views here.

   def index(request):
     return render_to_response('myapp/index.html', {'message': 'Hello'})

In the beginning of this file, there are import examples which you may
often use, so you can copy/paste these lines if you need. In the body,
there is a view function.

Basically, with Kay, you're supposed to write functions for
implementing application logics. Actually, view can be an object which
has a __call__() method (that means callable), but in this tutorial,
we define just functions for a time being.

index(request):

   View functions must be receive a ``Request`` object as its first
   argument. According to your configuration, a view function can have
   additional keyword argument, though index() method here is not.

   View functions must return a ``Response`` object. In the first
   example, we use a function ``render_to_response`` which is for
   creating a ``Response`` object from an html template and context
   values.


myapp/templates/index.html
==========================

The last one is an html template.

.. code-block:: html

   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
   <html>
   <head>
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
   <title>Top Page - myapp</title>
   </head>
   <body>
   {{ message }}
   </body>
   </html>

A template engine which is used in Kay is jinja2. Please remember
following two things about jinja2 first.

* To display a context value passed from your view, wrap a name of the
  value with ``{{}}``. You can call functions by adding
  parenthesis(and of course you can add arguments inside the
  parenthessis) as well as just displaying the value.

* You can use ``{% %}`` style tags for describing control structures and commands to jinja2 like ``{% if ... %} {% else %} {% endif %}``,  for loops, and ``{% extends "base_templates.html" %}``.

Here is an example usage of ``{% if %}``.

.. code-block:: html

   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
   <html>
   <head>
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
   <title>Top Page - myapp</title>
   </head>
   <body>
   {% if message %}
     <div id="message">
       {{ message }}
     </div>
   {% endif %}
   </body>
   </html>

In above example, we wrap a displaying part of a message with a 'div',
and using ``{% if %}`` allows us to display the message div only when
the message has a certain value.

Please keep in mind these two syntaxes for the time being.

Authentication
--------------

To enable the user authentication feature, youo need to install a middleware for authentication. Kay has various authentication backends. We'll use an authentication backend for Google Account in this tutorial.


Configuration
=============

First, you need to add ``MIDDLEWARE_CLASES`` including
``kay.auth.middleware.AuthenticationMiddleware``. 

.. code-block:: python

   MIDDLEWARE_CLASSES = (
     'kay.auth.middleware.AuthenticationMiddleware',
   )

Don't forget the comma after the middleware definition because when a
tuple has only one element, you need to place a comma after the
element explicitly.

After that, the auth module certainly work properly, I'd recommend you
define a model for storing information of a user. If you want to have
additional information later and so on, you can easily do this by your
own model.

If you use the authentication against Google Account and you want to
define own model, you need to extend ``kay.auth.models.GoogleUser``
and set the name of this extended model to
``settings.AUTH_USER_MODEL`` as a string.

myapp.models:

.. code-block:: python

   from google.appengine.ext import db
   from kay.auth.models import GoogleUser

   class MyUser(GoogleUser):
     pass

settings.py

.. code-block:: python

   AUTH_USER_MODEL = 'myapp.models.MyUser'


How to use
==========

request.user
++++++++++++

Once you enable the authentication middleware, it will add ``user``
attribute to the request object. If a user visiting web sites are
signed in, the content of the user attribute is an entity of the User
model, otherwise an instance of a class
``kay.auth.models.AnonymousUser``.

Here are common attributes and methods between those classes.

* is_admin

  This attribute indicates if the user is an administrator as a
  boolean value.

* is_anonymous()

  This method returns False if the user is signed in, otherwise, True.

* is_authenticated()

  This method returns True if the user is signed in, otherwise, False.


An example usage in template
++++++++++++++++++++++++++++

Let's put a fragment of code like following.

.. code-block:: html

   <div id="greeting">
     {% if request.user.is_anonymous() %}
       <a href="{{ create_login_url() }}">login</a>
     {% else %}
       Hello {{ request.user }}! <a href="{{ create_logout_url() }}">logout</a>
     {% endif %}
   </div>

This part of code will show a link for the login screen if the user
doesn't sign in, otherwise, a link for signing out.

Decorators
++++++++++

To protect a page from anonymous access, you can use following
decorators.  You can use ``kay.auth.decorators.login_required`` for
the page needs just an authorization and can use
``kay.auth.decorators.admin_required`` if the page has an admin
restriction.

Example:

.. code-block:: python

   from kay.utils import render_to_response
   from kay.auth.decorators import login_required

   # Create your views here.

   @login_required
   def index(request):
     return render_to_response('myapp/index.html', {'message': 'Hello'})

Let's confirm that you're recested to sign in when accessing the index
page.

ゲストブックの実装 - Step 1


Guestbook implementation - Step 1
---------------------------------

In this tutorial, we're gonna create a simple guestbook. I will
introduce various features as much as possible thorough out the
tutorial.

Firstly, let's look through a basic usage of Models ans Forms.

Model Definition
================

To define models, you can basically use appengine's db module
directly. Additionally there are special properties in ``kay.db``
package.

Here is a simple model for the guestbook.

myapp/models.py:

.. code-block:: python

   from google.appengine.ext import db
   from kay.auth.models import GoogleUser
   import kay.db

   # ...

   class Comment(db.Model):
     user = kay.db.OwnerProperty()
     body = db.TextProperty(required=True)
     created = db.DateTimeProperty(auto_now_add=True)

``kay.db.OwnerProperty`` which is difined in an attribute ``usser`` is
a property specially offerred by Kay. This is a property for storing a
key of a user who sines in automatically.

``body`` is a property for storing comment body itself, and
``created`` stores a date at which the comment is created
automatically.


Form definition
===============

Next, let's create a form for comment submission. Certainly you can
write an html form directly in your html templates, considering a
validation, I'd recommend you to create your form by using
``kay.utils.forms`` package.

There is no restriction about where to define your forms though,
``myapp/forms.py`` is one of appropriate places.

myapp/forms.py:

.. code-block:: python

   # -*- coding: utf-8 -*-

   from kay.utils import forms

   class CommentForm(forms.Form):
     body = forms.TextField("Your Comment", required=True)

You can define a form by creating a class that extends
``kay.utils.forms.Form``. In this example, ``body`` is an instance of
``form.TextField`` class. The first argument will become a label of a
generated form. If you specify ``required`` as True, the field will be
a mandatry field.

For more details about this form library, please refer to a `document
<http://kay-docs-jp.shehas.net/forms_reference.html>`_ about
``kay.utils.forms`` package.


View definition
===============

Let's write a view with these models and forms.

myapp/views.py:

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   myapp.views
   """

   from werkzeug import redirect

   from kay.utils import (
     render_to_response, url_for
   )
   from kay.auth.decorators import login_required

   from myapp.models import Comment
   from myapp.forms import CommentForm

   # Create your views here.

   @login_required
   def index(request):
     form = CommentForm()
     if request.method == "POST" and form.validate(request.form):
       comment = Comment(body=form['body'])
       comment.put()
       return redirect(url_for('myapp/index'))
     return render_to_response('myapp/index.html',
			       {'form': form.as_widget()})

You can see the new import statement of four lines:
``werkzeug.redirect``, ``kay.utils.url_for``, and newly created models
and forms. You can see that this view creates a form and validate
values from a form if the request method is POST.

After the validation succeeds, this view creates a new entity of
``Comment``, and redirect to the top page.

``url_for`` is a function for URL reverse lookup, and returns a URL
for an endpoint which is given as an argument. Let's look back the
default urls.py.

.. code-block:: python

   view_groups = [
     ViewGroup(
       Rule('/', endpoint='index', view='myapp.views.index'),
     )
   ]

In this ``urls.py``, we set 'index' as an endpoint. Hawever, when it
comes to reverse lookup, we used 'myapp/index'. Actually Kay adds an
application name and a slash to an endpoint automatically in order to
avoid conflicts between endpoints from multiple applications.

So, you need to specify an endpoint like ``app_name/endpoint``.


Template
========

.. code-block:: html

   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
   <html>
   <head>
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
   <title>Top Page - myapp</title>
   </head>
   <body>
     <div id="greeting">
       {% if request.user.is_anonymous() %}
	 <a href="{{ create_login_url() }}">login</a>
       {% else %}
	 Hello {{ request.user }}! <a href="{{ create_logout_url() }}">logout</a>
       {% endif %}
     </div>

     <div id="main_form">
       {{ form()|safe }}
     </div>
   </body>
   </html>

Now you can store comments submitted from the form to the datastore.

Let's try submitting on the development server. After submitting some
comments, you can visit http://localhost:8080/_ah/admin for viewing
contents of the datastore.

kind が ``myapp_comment`` というのが今回作成したコメントのエンティティ
です。kind にもアプリケーション名が前置されている事がわかります。デフォ
ルトでは Kay は クラス名 にアプリケーション名を前置して、さらに
lowercase したものを kind として使用します。この挙動を抑制するには
``settings.py`` にて ``ADD_APP_PREFIX_TO_KIND`` を False に設定します。

ゲストブックの実装 - Step 2
---------------------------

現在の実装だと投稿しても表示されないので実感がわきません。そこで最新20
件のコメントを表示するようにしてみましょう。

クエリーを使用する
==================

myapp/views.py:

.. code-block:: python

   ITEMS_PER_PAGE = 20

   # Create your views here.

   @login_required
   def index(request):
     form = CommentForm()
     if request.method == "POST" and form.validate(request.form):
       comment = Comment(body=form['body'])
       comment.put()
       return redirect(url_for('myapp/index'))
     query = Comment.all().order('-created')
     comments = query.fetch(ITEMS_PER_PAGE)
     return render_to_response('myapp/index.html',
			       {'form': form.as_widget(),
				'comments': comments})

このコードでは、テンプレートに対して、最新20件のコメントを渡しています。

テンプレート内でのループ
========================

テンプレートで受け取ったコメントを表示しましょう。

myapp/templates/index.html:

.. code-block:: html

  {% if comments %}
    <div id="comment_list">
      <ul>
      {% for comment in comments %}
        <li>{{ comment.body }}
          <span class="author"> by {{ comment.user }}</span>
      {% endfor %}
      </ul>
    </div>
  {% endif %}

フォームを表示している部分の下に上記コードを追加しましょう。これで最新
20件のコメントが表示されるようになりました。

ゲストブックの実装 - Step 3
---------------------------

コメント投稿時に予め設定してあるカテゴリーを選べるようにしましょう。

モデルフォーム
==============

まずはカテゴリーを保存するモデルを作り ``Comment`` クラスにもプロパティ
を追加しましょう。

myapp/models.py:

.. code-block:: python

   class Category(db.Model):
     name = db.StringProperty(required=True)

     def __unicode__(self):
       return self.name

   class Comment(db.Model):
     user = kay.db.OwnerProperty()
     category = db.ReferenceProperty(Category)
     body = db.StringProperty(required=True, verbose_name=u'Your Comment')
     created = db.DateTimeProperty(auto_now_add=True)


次にフォームですが、プロパティが増える度にフォームの実装も変更しなけれ
ばならないのは面倒なので、モデルからフォームを自動生成できる仕組みを使
いましょう。

モデルからフォームを自動生成するには
``kay.utils.forms.modelform.ModelForm`` クラスを継承したフォームを作成
します。

.. code-block:: python

   # -*- coding: utf-8 -*-

   from kay.utils import forms
   from kay.utils.forms.modelform import ModelForm

   from myapp.models import Comment

   class CommentForm(ModelForm):
     class Meta:
       model = Comment
       exclude = ('user', 'created')

``ModelForm`` の使いかたはまず ``ModelForm`` を継承したクラスを作成しま
す。次にその中に内部クラス ``Meta`` を定義する事で設定を行います。
``Meta`` 内で有効な attribute は下記の通りです。

* model

  フォーム生成の元にするモデルクラスを指定します。

* exclude

  モデルクラスに定義されているプロパティの中で、フォームに表示しないも
  のをタプルで指定します。次の ``fields`` とは排他的で、どちらか一方し
  か設定できません。

* fields

  モデルクラスに定義されているプロパティの中で、フォームに表示するもの
  をタプルで指定します。 ``fields`` に定義されていないプロパティは表示
  されません。上記の ``exclude`` とは排他的で、どちらか一方しか設定でき
  ません。

* help_texts

  フォームフィールドにヘルプ文字列を与える時に使用します。フィールドの
  名前をキーにした辞書として設定します。

管理用スクリプト
================

この段階で、カテゴリーを選ぶフォームはできているのですが、まだカテゴリー
がありませんので、セレクトボックスには選択肢がありません。これは少し寂
しいので、カテゴリーを追加しましょう。ここでは、カスタムの管理用スクリ
プトを追加してカテゴリーを追加できるようにしてみます。

``myapp/management.py`` というファイルを下記の内容で作成しましょう。

.. code-block:: python

   # -*- coding: utf-8 -*-

   from google.appengine.ext import db

   from kay.management.utils import (
     print_status, create_db_manage_script
   )
   from myapp.models import Category

   categories = [
     u'Programming',
     u'Testing',
     u'Management',
   ]

   def create_categories():
     entities = []
     for name in categories:
       entities.append(Category(name=name))
     db.put(entities)
     print_status("Categories are created successfully.")

   def delete_categories():
     db.delete(Category.all().fetch(100))
     print_status("Categories are deleted successfully.")

   action_create_categories = create_db_manage_script(
     main_func=create_categories, clean_func=delete_categories,
     description="Create 'Category' entities")

うまくできると、 ``python manage.py`` の出力に下記のエントリが追加され
ます::

  create_categories:
    Create 'Category' entities

    -a, --appid                   string    
    -h, --host                    string    
    -p, --path                    string    
    --no-secure
    -c, --clean

下記のようにして ``Category`` のエンティティを三つ追加できます。

* GAE にデプロイしたアプリに対して実行するには

  $ python manage.py create_categories

* 起動している開発用サーバーに対して実行するには

  $ python manage.py create_categories -h localhost:8080 --no-secure

``Category`` を追加した後で、アプリケーションにアクセスしてみましょう。
三つの選択肢が選べるようになっていれば成功です。

いくつかコメントをカテゴリを指定して投稿し、データストアビューアーで確
認してみましょう。

.. Note::

   管理用スクリプトを追加する方法について詳しく知るには `カスタムの管理
   用スクリプトを書く方法
   <http://kay-docs-jp.shehas.net/manage_py.html#id4>`_ を参考にしてく
   ださい。


カテゴリーの表示
================

コメントの一覧にカテゴリーを表示するようにしてみましょう。コメントの一
覧を表示している部分を下記のように変更します。

.. code-block:: python

     {% if comments %}
       <div id="comment_list">
	 <ul>
	 {% for comment in comments %}
	   <li>{{ comment.body }}
	     <span class="author"> by {{ comment.user }}</span>
	     {% if comment.category %}
	       <br>
	       <span class="category"> in {{ comment.category.name }}</span>
	     {% endif %}
	 {% endfor %}
	 </ul>
       </div>
     {% endif %}


CRUDの自動生成
==============

次にこのカテゴリを管理する画面を作成してみます。管理者のみがアクセス可
能な、カテゴリの追加・削除・変更ができる画面を作成します。

まず ``Category`` 用のフォームを作成します。

myapp/forms.py:

.. code-block:: python

   # -*- coding: utf-8 -*-

   from kay.utils import forms
   from kay.utils.forms.modelform import ModelForm

   from myapp.models import (
     Comment, Category
   )

   class CommentForm(ModelForm):
     class Meta:
       model = Comment
       exclude = ('user', 'created')

   class CategoryForm(ModelForm):
     class Meta:
       model = Category

``Category`` をインポートし、新たに ``CategoryForm`` を定義しています。

次に myapp/urls.py を下記のように変更します。

.. code-block:: python

   from kay import generics
   from kay.routing import (
     ViewGroup, Rule
   )

   class CategoryCRUDViewGroup(generics.CRUDViewGroup):
     model = 'myapp.models.Category'
     form = 'myapp.forms.CategoryForm'
     authorize = generics.admin_required

   view_groups = [
     ViewGroup(
       Rule('/', endpoint='index', view='myapp.views.index'),
     ),
     CategoryCRUDViewGroup(),
   ]

最後に ``settings.py`` の ``MIDDLEWARE_CLASSES`` に
``kay.utils.flash.FlashMiddleware`` を追加します。

.. code-block:: python

   MIDDLEWARE_CLASSES = (
     'kay.auth.middleware.AuthenticationMiddleware',
     'kay.utils.flash.FlashMiddleware',
   )

これで http://localhost:8080/category/list にアクセスするとカテゴリーの
リストが表示されるはずです。追加や編集などを試してみてください。

.. Note::

   CRUDの自動生成について、さらに詳しくは `汎用ビューグループ
   <http://kay-docs-jp.shehas.net/generic_views.html>`_ をご覧下さい。


カテゴリー削除時の対処
======================

既に気づいた方もいらっしゃるかも知れませんが、この段階で、コメントが一
つ以上属しているカテゴリーを削除すると、コメントの表示時にエラーになっ
てしまいます。

ここでは、カスケードデリートを実装するために ``db_hook`` の仕組みを使用
しましょう。

もしエラーになってしまった方は、当該のコメントをデータストアビューアー
から消去するか、開発用サーバーを一度止めて ``python manage.py
runserver -c`` と -c を付けてデータを全削除し、再度カテゴリー・コメント
を作成してから進んでください。


まずは ``settings.py`` で ``db_hook`` の仕組みを有効にします。

.. code-block:: python

   USE_DB_HOOK = True

次に下記のようにして myapp/__init__.py でフック関数を登録します。

myapp/__init__.py:

.. code-block:: python

   # -*- coding: utf-8 -*-
   # Kay application: myapp

   from google.appengine.ext import db

   from kay.utils.db_hook import register_pre_delete_hook

   from myapp.models import (
     Comment, Category
   )

   def cascade_delete(key):
     entities = Comment.all(keys_only=True).filter('category =', key).fetch(2000)
     db.delete(entities)

   register_pre_delete_hook(cascade_delete, Category)

ここでは ad-hoc に 2000 件のみ取得して消去していますが、実際にきちんと
実装するにはもう少しがんばってください。

この状態でカテゴリーを消去すると、そのカテゴリーに属するコメントもそれ
に伴って削除されるはずです。

.. Note::

   db_hook 機能についてさらに詳しくは `db_hook 機能を使用する
   <http://kay-docs-jp.shehas.net/db_hook.html>`_ をご覧下さい。


ゲストブックの実装 - Step 4
---------------------------

次にアプリケーションを国際化してみましょう。Kay では gettext ベースの国
際化機能が備わっています。

国際化を有効にする
==================

まずは ``settings.py`` で ``USE_I18N`` を True に設定します。

.. code-block:: python

   USE_I18N = True

この段階で、中途半端に国際化されている事と思います。accept_language で
日本語を優先した状態でアクセスすると、トップページの ``submit`` が ``送
信`` に変わっている事がわかります。

国際化のためにメッセージをマークする
====================================

まずはフォームに表示するフィールドのタイトルをマークします。

myapp/models.py:

.. code-block:: python

   # -*- coding: utf-8 -*-
   # myapp.models

   from google.appengine.ext import db
   from kay.auth.models import GoogleUser
   import kay.db
   from kay.i18n import lazy_gettext as _

   # Create your models here.

   class MyUser(GoogleUser):
     pass

   class Category(db.Model):
     name = db.StringProperty(required=True, verbose_name=_(u'Name'))

     def __unicode__(self):
       return self.name

   class Comment(db.Model):
     user = kay.db.OwnerProperty()
     category = db.ReferenceProperty(Category, verbose_name=_(u'Category'))
     body = db.StringProperty(required=True, verbose_name=_(u'Your Comment'))
     created = db.DateTimeProperty(auto_now_add=True)

``kay.i18n.lazy_gettext`` を ``_`` として import しています。更にフォー
ムに表示するフィールドには ``verbose_name`` という引数を渡すようにして、
値を ``_()`` の呼び出しで囲んでおきます。

.. Note::

   詳しくは説明しせんが、大雑把に言うと models.py や forms.py では
   ``lazy_gettext`` を使用します。views.py の中では ``gettext`` を使用
   します。

次はテンプレート内部の文字列をマークしましょう。ここでは練習のため二つ
の方法を試します。

myapp/templates/index.html:

.. code-block:: html

     <div id="greeting">
       {% if request.user.is_anonymous() %}
	 <a href="{{ create_login_url() }}">{{ _('login') }}</a>
       {% else %}
	 Hello {{ request.user }}! <a href="{{ create_logout_url() }}">
	   {% trans %}logout{% endtrans %}
	 </a>
       {% endif %}
     </div>

翻訳を作成する
==============

下記のコマンドでマークした文字列を抽出します。

.. code-block:: bash

   $ python manage.py extract_messages -a
   Running on Kay-0.10.0
   Extracting from /Users/tmatsuo/work/kay-tutorial/myproject/myapp
   myapp/__init__.py
   myapp/forms.py
   myapp/management.py
   myapp/models.py
   myapp/urls.py
   myapp/views.py
   myapp/templates/index.html
   All done.

日本語用の po ファイルを作成します。

.. code-block:: bash

   $ python manage.py add_translations -a -l ja
   Running on Kay-0.10.0
   Creating myapp/i18n/ja/LC_MESSAGES/messages.po.
   Cant open file. Skipped myapp/i18n/jsmessages.pot.
   Created catalog for ja
   Cant open file. Skipped /Users/tmatsuo/work/kay-tutorial/myproject/i18n/messages.pot.
   Cant open file. Skipped /Users/tmatsuo/work/kay-tutorial/myproject/i18n/jsmessages.pot.
   Created catalog for ja

myapp/i18n/ja/LC_MESSAGES/messages.po をエディタで編集します。

.. code-block:: po

   # Japanese translations for PROJECT.
   # Copyright (C) 2010 Takashi Matsuo
   # This file is distributed under the same license as the PROJECT project.
   # FIRST AUTHOR <EMAIL@ADDRESS>, 2010.
   #
   msgid ""
   msgstr ""
   "Project-Id-Version: myproject-0.1\n"
   "Report-Msgid-Bugs-To: tmatsuo@candit.jp\n"
   "POT-Creation-Date: 2010-05-06 16:39+0900\n"
   "PO-Revision-Date: 2010-05-06 16:39+0900\n"
   "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
   "Language-Team: ja <LL@li.org>\n"
   "Plural-Forms: nplurals=1; plural=0\n"
   "MIME-Version: 1.0\n"
   "Content-Type: text/plain; charset=utf-8\n"
   "Content-Transfer-Encoding: 8bit\n"
   "Generated-By: Babel None\n"

   #: myapp/models.py:15
   msgid "Name"
   msgstr "カテゴリー名"

   #: myapp/models.py:22
   msgid "Category"
   msgstr "カテゴリー"

   #: myapp/models.py:23
   msgid "Your Comment"
   msgstr "コメント"

   #: myapp/templates/index.html:11
   msgid "login"
   msgstr "ログイン"

   #: myapp/templates/index.html:14
   msgid "logout"
   msgstr "ログアウト"

.. Note::

   このファイルは文字コードを UTF-8 で保存してください。

上記のように編集した後に、このファイルをコンパイルします。

.. code-block:: bash

   $ python manage.py compile_translations -a
   Running on Kay-0.10.0
   Compiling myapp/i18n
   Compiling myapp/i18n/ja/LC_MESSAGES/messages.po 
   All done.
   i18n folder missing

これでアプリケーションにアクセスすれば、翻訳文字列を準備した場所では日
本語が表示されているはずです。
