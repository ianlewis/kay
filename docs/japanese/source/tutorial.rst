==================
Kay チュートリアル
==================

まずは簡単な掲示板を作るチュートリアルをご紹介します。

準備
----

下記のものをインストールします。

* Python-2.5
* App Engine SDK/Python
* Kay Framework
* ipython (推奨)

macports の python25 を使うばあいは、他に下記もインストールしましょう。

* py25-hashlib
* py25-socket-ssl
* py25-pil
* py25-ipython (推奨)

今回は Kay のリポジトリバージョンを使います。それには Mercurial が必要です。

* mercurial

下記のようにして clone できます。

.. code-block:: bash

  $ hg clone https://kay-framework.googlecode.com/hg/ kay

もしリリースバージョンを使う場合は http://code.google.com/p/kay-framework/downloads/list から最新版をダウンロードして下記のように解凍します。

.. code-block:: bash

   $ tar zxvf kay-VERSION.tar.gz


もし zip 版の appengine SDK をインストールした場合は、下記のようにシンボリックリンクを作ってください。

.. code-block:: bash

   $ sudo ln -s /some/whare/google_appengine /usr/local/google_appengine    


プロジェクトの開始
------------------

新しいプロジェクトを始めるには、kay の ``manage.py`` スクリプトでプロジェクトディレクトリの雛型を作成します。

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

シンボリックリンクをサポートしているプラットフォームでは kay ディレクトリと ``manage.py`` へのシンボリックリンクが作成されます。後で kay の場所を動かすときっと動かなくなるのですが、そんな時はリンクを張り直してください。

アプリケーションを作る
----------------------

出来たばかりの ``myproject`` ディレクトリに ``cd`` して、早速アプリケーションを作りましょう。下記の例では ``myapp`` というアプリケーションを作成しています。

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

アプリケーションが出来たら ``settings.py`` を編集して、プロジェクトに登録します。
まずは ``settings.py`` の ``INSTALLED_APPS`` に ``myapp`` を追加します。必要なら ``APP_MOUNT_POINTS`` も設定してください。下記の例では、アプリケーションをルート URL にマウントする例です。
``APP_MOUNT_POINTS`` を設定しない場合は ``/myapp`` というようにアプリケーション名 URL にマウントされます。
なお、ここでは ``kay.auth`` というアプリケーションも一緒に登録しています。


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


ご覧になれば分かると思いますが ``INSTALLED_APPS`` はタプルで ``APP_MOUNT_POINTS`` は dict になっています。

アプリケーションを動かす
------------------------

作ったアプリケーションを動かしてみましょう。下記のコマンドで開発サーバが起動する筈です。

.. code-block:: bash

  $ python manage.py runserver
  INFO     2009-08-04 05:48:21,339 appengine_rpc.py:157] Server: appengine.google.com
  ...
  ...
  INFO     ... Running application myproject on port 8080: http://localhost:8080


この状態で http://localhost:8080/ にアクセスすると、「Hello」又は「こんにちは」と表示される筈です。


GAE にアップロードする
----------------------

GAE にアップロードするには、対象の ``appid`` を ``app.yaml`` の ``application`` に設定してから、下記のコマンドを使用します。

.. code-block:: bash

  $ python manage.py appcfg update

成功すると、http://your-appid.appspot.com/ でアクセスできるようになります。

テンプレート／ビュー
--------------------

デフォルトのビューとテンプレートを見てみましょう。

myapp/views.py

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.views

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

  # Create your views here.

  def index(request):
    return render_to_response('myapp/index.html', {'message': _('Hello')})

デフォルトのビューがひとつ定義されています。
:func:`kay.utils.render_to_response()` 関数は第一引数にテンプレート名を受け取ります。第二引数にはテンプレートに渡す辞書を渡せます。
``_()`` という関数は国際化のために文字列をマークし、表示の時には実際に国際化するための関数です。

``myapp/index.html`` が実際に指すテンプレートは、myapp/templates/index.html にあります(/templates/ が間に挟まっている事に注意してください)。

myapp/templates/index.html

.. code-block:: html

  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">
  <html>
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Top Page - myapp</title>
  </head>
  <body>
  {{ message }}
  </body>
  </html>

``{{ message }}`` の部分に :func:`kay.utils.render_to_response()` の第二引数で渡した ``message`` が表示される事になります。


url mapping
-----------

次に URL とビューの対応を設定するファイルを見てみます。

myapp/urls.py

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.urls


  from werkzeug.routing import (
    Map, Rule, Submount,
    EndpointPrefix, RuleTemplate,
  )
  import myapp.views

  def make_rules():
    return [
      EndpointPrefix('myapp/', [
	Rule('/', endpoint='index'),
      ]),
    ]

  all_views = {
    'myapp/index': myapp.views.index,
  }


この ``urls.py`` で定義された ``make_rules()`` 関数と ``all_views`` 辞書は、Kay により自動的に収集され、設定されます。

``make_rules`` の方では ``'/'`` という URL を ``'myapp/index'`` という endpoint に結びつけていて ``all_views`` の方では ``'myapp/index'`` という endpoint を ``myapp.views.index`` 関数に対応づけています。

これにより ``'/'`` へのアクセス時に ``myapp.views.index`` が呼出されるわけです。

``'/'`` -> ``'myapp/index'`` -> ``myapp.views.index``

ユーザー認証
------------

ユーザー認証を使用する方法はいくつかありますが、ここでは Google Account での認証を使ってみましょう。デフォルトの ``settings.py`` では Google Account の認証を使用するようになっていますが、認証用のミドルウェアを有効にする必要があります。

.. code-block:: python

  MIDDLEWARE_CLASSES = (
    'kay.auth.middleware.AuthenticationMiddleware',
  )

``myapp/templates/index.html`` を編集して、下記のようにすると、ユーザー認証を使用する事ができます。

.. code-block:: html

  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">
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
  {{ message }}
  </body>
  </html>


上記のコードでは、ユーザーがログインしていない場合は、ログインフォームへのリンクを表示し、ログイン済みの場合は user のメールアドレスと、ログアウトリンクを表示します。

開発環境と GAE の両方で試してみましょう。

この段階ですと、ユーザーはログインせずとも ``myapp.index`` を閲覧する事ができます。これをログインした場合だけ閲覧できるようにするには、どうすれば良いでしょうか。

これは、下記のように ``myapp.views.index`` にデコレーターを付ける事で可能です。

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.views
  # ...
  # ...
  # Create your views here.

  @login_required
  def index(request):
    return render_to_response('myapp/index.html', {'message': _('Hello')})

``login_required`` デコレーターで修飾すれば、そのビューはログインしていないと閲覧できなくなり、自動的にログインフォームへ飛ばされるようになります。

ここでは一度動作を確認した後で、このデコレーターは外しておきましょう。


モデル定義
----------

それでは datastore にコメントを投稿できるようにしてみましょう。まずはコメントを保存するためのモデルを定義します。

myapp/models.py

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.models

  from google.appengine.ext import db

  # Create your models here.

  class Comment(db.Model):
    user = db.ReferenceProperty()
    body = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

モデルは ``google.appengine.ext.db.Model`` を継承したクラスを作成する事により定義します。クラス変数を定義する事により属性を定義できます。ここでは ``user`` にコメント主を ``body`` に内容を ``created`` に投稿日時を保存する事にしました。

このモデルにデータを保存してみましょう。ここでは Kay の shell ツールを使ってデータを保存します。

.. code-block:: bash

  $ python manage.py shell
  Running on Kay-0.0.0
  In [1]: c1 = Comment(body='Hello, guestbook')
  In [2]: c1.put()
  Out [2]: datastore_types.Key.from_path(u'myapp_comment', 1, _app_id_namespace=u'myproject')
  In [3]: c1.body
  Out[3]: u'Hello, guestbook'
  In [4]: ^D
  Do you really want to exit ([y]/n)? y

^D は Ctrl + D です。
``put()`` を忘れると保存出来ませんので注意してください。shell ツールで登録したデータは開発サーバーを再起動しないと反映されませんので開発サーバーを再起動します。再起動後、データが保存されているかどうか http://localhost:8080/_ah/admin/ にアクセスして確認してみましょう。

データを表示する
----------------

今保存した Comment を表示してみましょう。二つのファイルを編集します。

myapp/views.py

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.views
  # ...
  # ...
  from models import Comment

  # Create your views here.

  def index(request):
    comments = Comment.all().order('-created').fetch(100)
    return render_to_response('myapp/index.html',
			      {'message': _('Hello'),
			       'comments': comments})

先程定義したモデルクラスを import するのを忘れないようにしましょう。
``Comment.all().order('-created').fetch(100)`` で、データストアから最新 100 件のコメントを取得し、そのリストを ``render_to_response`` に渡しています。 :func:`kay.utils.render_to_response()` も参照してください。

myapp/templates/index.html

.. code-block:: html

  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">
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
  {{ message }}
  <div>
  {% for comment in comments %}
  <hr/>
  {{ comment.body }}&nbsp;by&nbsp;<i>{{ comment.user }}</i>
  {% endfor %}
  </div>
  </body>
  </html>

``message`` を表示している下に、新しく div を追加しています。
``{% for ... %}`` と ``{% endfor %}`` はループです。ここでは ``comment.body`` と投稿者を表示するだけです。

コメント投稿フォーム
--------------------

コメントを投稿できるようにしましょう。html のフォームのために ``myapp`` ディレクトリ内に ``forms.py`` というファイルを新規に作成します。

myapp/forms.py

.. code-block:: python

  from kay.i18n import lazy_gettext as _
  from kay.utils import forms


  class CommentForm(forms.Form):
    comment = forms.TextField(_("comment"), required=True)

``kay.utils.forms.Form`` を拡張したクラスを定義して、フィールドをひとつ定義します。このフォームを表示するためにビューとテンプレートを編集します。

myapp/views.py

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.views
  #...
  #...
  from models import Comment
  from forms import CommentForm

  # Create your views here.

  def index(request):
    comments = Comment.all().order('-created').fetch(100)
    form = CommentForm()
    if request.method == 'POST':
      if form.validate(request.form):
	if request.user.is_authenticated():
	  user = request.user
	else:
	  user = None
	new_comment = Comment(body=form['comment'],user=user)
	new_comment.put()
	return redirect('/')
    return render_to_response('myapp/index.html',
			      {'message': _('Hello'),
			       'comments': comments,
			       'form': form.as_widget()})


POST 値にアクセスするには ``request.form`` を使用します。GET のパラメーターは ``request.args`` で取得できます。またアップロードされたファイルにアクセスするには ``request.files`` を使用します。

myapp/templates/index.html

.. code-block:: html

  <div>
  {{ form()|safe }}
  </div>

ここまでで、コメントを投稿できるようになります。コメントの脇には誰が投稿したかも表示されますね。

