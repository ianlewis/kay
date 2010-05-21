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

Don't forget the comma after middleware definition because you need to
place a comma after the element explicitly when a tuple has only one
element.

このままでも認証自体は動くのですが、さらにユーザー情報を入れるモデルを
自分で定義する事をお勧めします。後でユーザーに紐付く情報を殖やしたくなっ
た時など、独自のモデルを定義しておいた方が何かと楽です。

Google Account での認証を行う場合は ``kay.auth.models.GoogleUser`` を継
承したモデルを定義し、そのモデル名を ``settings.py`` の
``AUTH_USER_MODEL`` に記載します(文字列で構いません)。

myapp.models:

.. code-block:: python

   from google.appengine.ext import db
   from kay.auth.models import GoogleUser

   class MyUser(GoogleUser):
     pass

settings.py

.. code-block:: python

   AUTH_USER_MODEL = 'myapp.models.MyUser'

ここでは、モデルにはまだ独自プロパティを定義していませんが、将来のため
に始めから独自モデルにしておく事をお勧めします。

使用方法
========

request.user
++++++++++++

認証用ミドルウェアを有効にすると ``request.user`` が設定されます。ユー
ザーがログインしていればユーザーエンティティ、そうでなければ
``kay.auth.models.AnonymousUser`` というクラスのインスタンスが入ってい
ます。

これらのクラスに共通して使用できるアトリビュートとメソッドを示します。

* is_admin

  このアトリビュートは、そのユーザーが管理者かどうかを表す真偽値です。

* is_anonymous()

  このメソッドはユーザーがログインしていれば False をログインしてなけれ
  ば True を返します。

* is_authenticated()

  ログインしていれば True, そうでなければ False を返します。


template 内での使用例
+++++++++++++++++++++

下記のような断片を ``myapp/templates/index.html`` に入れてみましょう。

.. code-block:: html

   <div id="greeting">
     {% if request.user.is_anonymous() %}
       <a href="{{ create_login_url() }}">login</a>
     {% else %}
       Hello {{ request.user }}! <a href="{{ create_logout_url() }}">logout</a>
     {% endif %}
   </div>

このコードは、ユーザーがログインしていなければログイン画面へのリンクを
表示し、ログインしていればログアウトするためのリンクを表示します。

デコレーター
++++++++++++

認証しないとアクセスできないページを簡単に作るには、デコレーターを使い
ます。ログインしないとアクセスできないようにするには
``kay.auth.decorators.login_required`` で、管理者アカウントにてログイン
が必要なページを作成するには、 ``kay.auth.decorators.admin_required``
で view 関数を修飾します。

例:

.. code-block:: python

   from kay.utils import render_to_response
   from kay.auth.decorators import login_required

   # Create your views here.

   @login_required
   def index(request):
     return render_to_response('myapp/index.html', {'message': 'Hello'})

index へのアクセス時にログインが必要になっている事を確認してみましょう。

ゲストブックの実装 - Step 1
---------------------------

このチュートリアルでは簡単なゲストブックを作成します。その過程で、Kay
の機能をできるだけ紹介していく予定です。

まずはモデルとフォームの基本的な使い方についてご紹介します。

モデル定義
==========

Kay でのモデル定義には基本的に appengine の db モジュールをそのまま使い
ます。 ``kay.db`` パッケージ内に少しだけ Kay 独自のプロパティがあります。

ここではゲストブック用のモデルを定義してみましょう。

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

``user`` に割り当てた ``kay.db.OwnerProperty`` は Kay 独自のプロパティ
で、現在ログイン中であるユーザーの key を自動で格納するためのプロパティ
です。

``body`` にはコメント本体を保存します。また ``created`` には作成日時が
自動で入ります。


フォーム定義
============

次に投稿用のフォームを作ります。テンプレート内に直に html フォームを書
いても動かす事はできますが、値の検証などの事も考えると
``kay.utils.forms`` パッケージを使用してフォームを作成した方が良いでしょ
う。

フォーム定義の場所に特にきまりはありませんが ``myapp/forms.py`` に定義
しましょう。

myapp/forms.py:

.. code-block:: python

   # -*- coding: utf-8 -*-

   from kay.utils import forms

   class CommentForm(forms.Form):
     body = forms.TextField("Your Comment", required=True)

``kay.utils.forms.Form`` を継承したクラスを定義する事によりフォームを作
成できます。このクラスでは ``body`` という名前で ``forms.TextField`` の
インスタンスを指定しています。初めの引数はフォームフィールドのラベルに
なります。 ``required`` に True を指定すると、このフィールドは入力が必
須になります。

他にどのようなフィールドがあるか、またそれらの使い方については
``kay.utils.forms`` パッケージについての `ドキュメント
<http://kay-docs-jp.shehas.net/forms_reference.html>`_ も参照してくださ
い。

ビュー定義
==========

これらのモデルとフォームを使用して投稿用のビューを書きましょう。

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

``werkzeug.redirect``, ``kay.utils.url_for`` と先程作成したモデル・フォー
ムを import しています。 ``index`` ビューの内部ではフォームを作成し、
http メソッドが POST の時にはフォームのバリデーションを行っています。

フォームのバリデーションに成功した場合には ``Comment`` オブジェクトを作
成した後に、トップページへリダイレクトしています。

``url_for`` というのは URL 逆引きのための関数で、引数で与えられた
endpoint に対応する URL を返します。ここでデフォルトの urls.py を思い返
してみましょう。

.. code-block:: python

   view_groups = [
     ViewGroup(
       Rule('/', endpoint='index', view='myapp.views.index'),
     )
   ]

urls.py では endpoint として 'index' を指定していました。ですが逆引きの
時には 'myapp/index' を使用しています。実は Kay ではアプリケーション間
で endpoint が衝突する事を防ぐために、自動でアプリケーション名を前置し
ます。

ですので、逆引きを行う時には ``urls.py`` で設定した endpoint そのままで
は無く ``app_name/endpoint`` という形で endpoint を指定する必要がありま
す。

テンプレート
============

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

ここまでで、フォームから投稿したコメントを datastore に保存できるように
なりました。

開発用サーバーでデータが保存できるか試してみましょう。いくつかコメント
を投稿した後に http://localhost:8080/_ah/admin へアクセスすると、データ
ストアの中身を見る事ができます。

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
