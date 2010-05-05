==================
汎用ビューグループ
==================

.. Note::

  この機能はまだ実験段階です。将来仕様が変わる可能性があります。

概要
----

``kay.generics.CRUDViewGroup`` を使用すると、汎用的な CRUD の view を簡
単に定義できます。CRUDViewGroup を使用するには、モデル・モデルフォーム・
テンプレートさえあれば良いです。


簡単な例
--------

一番単純な例を見てみましょう

myapp/models.py

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.models

  from google.appengine.ext import db

  # Create your models here.

  class MyModel(db.Model):
    comment = db.StringProperty()

    def __unicode__(self):
      return self.comment

ここで定義している ``__unicode__`` メソッドは簡単にこのモデルのエンティ
ティを表示するためのものです。デフォルトのテンプレートが表示のためにこ
のメソッドを使用しますので、独自テンプレートを使用して、他の方法で表示
するならば必要ありません。

myapp/forms.py

.. code-block:: python

  from kay.utils.forms.modelform import ModelForm

  from myapp.models import MyModel

  class MyForm(ModelForm):
    class Meta:
      model = MyModel

単純なモデルフォームです。

最低限これだけあれば、CRUD用のオブジェクトを作れます。ここでは
``urls.py`` に書きましょう。

myapp/urls.py

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.urls

  from kay import generics

  from myapp.forms import MyForm
  from myapp.models import MyModel

  class MyCRUDViewGroup(generics.CRUDViewGroup):
    model = MyModel
    form = MyForm

  view_groups = [MyCRUDViewGroup()]


これだけです。ただ下記のように ``kay.utils.flash.FlashMiddleware`` を追
加した方が便利なので追加しましょう。

settings.py

.. code-block:: python

  MIDDLEWARE_CLASSES = (
    'kay.utils.flash.FlashMiddleware',
  )

こうすると '/mymodel/list' にアクセスすれば ``MyModel`` のエンティティ
一覧を表示できます。下記は MyCRUDViewGroup で作られるデフォルトのマッピ
ングルールです。

.. code-block:: python

  Map([[<Rule '/mymodel/list' -> myapp/list_mymodel>,
   <Rule '/mymodel/list/<cursor>' -> myapp/list_mymodel>,
   <Rule '/mymodel/show/<key>' -> myapp/show_mymodel>,
   <Rule '/mymodel/create' -> myapp/create_mymodel>,
   <Rule '/mymodel/update/<key>' -> myapp/update_mymodel>,
   <Rule '/mymodel/delete/<key>' -> myapp/delete_mymodel>]])

``model`` と ``form`` class attribute には文字列も使用できます。文字列
で指定するとモジュールを遅延ロードできます。

myapp/urls.py

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.urls

  from kay import generics

  class MyCRUDViewGroup(generics.CRUDViewGroup):
    model = 'myapp.models.MyModel'
    form = 'myapp.forms.MyForm'

  view_groups = [MyCRUDViewGroup()]


独自のテンプレートを使用する
----------------------------

``templates`` class attribute を指定すれば、独自のテンプレートが使用で
きます。下記に例を示します:

.. code-block:: python

  class MyCRUDViewGroup(CRUDViewGroup):
    model = 'myapp.models.MyModel'
    form = 'myapp.forms.MyForm'
    templates = {
      'show': 'myapp/mymodel_show.html',
      'list': 'myapp/mymodel_list.html',
      'update': 'myapp/mymodel_update.html'
    }

デフォルトのテンプレートは下記のようになっています:

.. code-block:: python

  templates = {
    'list': '_internal/general_list.html',
    'show': '_internal/general_show.html',
    'update': '_internal/general_update.html',
  }

まずは手始めとして、 ``kay/_internal/tempaltes/general_***.html`` をア
プリケーションのテンプレートディレクトリにコピーして、それらを編集する
のが楽でしょう。

エンティティの作成・更新時に追加の属性を与える
----------------------------------------------

時には、エンティティの作成・更新時にモデルフォームで定義する以外の値を
渡したい事もあります。そのためには CRUDViewGroup のサブクラスに
``get_additional_context_on_create`` や
``get_additional_context_on_update`` インスタンスメソッドを定義します。

これらのメソッドは ``request`` と ``form`` インスタンスを引数として受け
取り、dict を返します。この dict は ModelForm の ``save()`` メソッドに
渡されます。


自動的に現在のユーザーをプロパティに保存する
--------------------------------------------

``kay.db.OwnerProperty`` を使用すると簡単に、現在のユーザーを保存できま
す。このプロパティのデフォルト値はユーザーがログインしていればそのユー
ザーの key で、そうでなければ None です。下記の例のように
``ModelForm`` ではこのプロパティは除外する必要があります:

myapp/models.py

.. code-block:: python

  # -*- coding: utf-8 -*-
  # myapp.models

  from google.appengine.ext import db
  from kay.db import OwnerProperty

  # Create your models here.

  class MyModel(db.Model):
    user = OwnerProperty()
    comment = db.StringProperty()

    def __unicode__(self):
      return self.comment

myapp/forms.py

.. code-block:: python

  from kay.utils.forms.modelform import ModelForm

  from myapp.models import MyModel

  class MyForm(ModelForm):
    class Meta:
      model = MyModel
      exclude = ('user',)

urls.py は変更しなくとも大丈夫です。


一覧に出すエンティティに対するフィルター
----------------------------------------

``CRUDViewGroup`` サブクラスの ``get_query`` メソッドを定義する事で、ど
のエンティティを一覧に表示するかコントロールできます。

下記の例では、現在ログイン中のユーザーが所有するエンティティのみ表示す
る事ができます。

.. code-block:: python

   class MyCRUDViewGroup(generics.CRUDViewGroup):
     model = 'myapp.models.MyModel'
     form = 'myapp.forms.MyForm'

     def get_query(self, request):
       return self.model.all().filter('user =', request.user.key()).\
         order('-created')

見て分かるとおり、 ``get_query`` は現在の ``request`` を引数として取り、
``Query`` インスタンスを返します。


アクセス制御
------------

特定の操作を特定のユーザー・グループに制限するには、 ``CRUDViewGroup``
サブクラスに ``authorize`` インスタンスメソッドを作成します。操作は
``list``, ``show``, ``create``, ``update``, ``delete`` に分類されていま
す。

``kay.generics`` パッケージには便利なプリセットの関数がいくつか用意され
ていて、これらの中から選んで使う事もできます。

* kay.generics.login_required
* kay.generics.admin_required
* kay.generics.only_owner_can_write
* kay.generics.only_owner_can_write_except_for_admin

下記の例ではこのうちの一つを使用しています:

.. code-block:: python

   class MyCRUDViewGroup(generics.CRUDViewGroup):
     model = 'myapp.models.MyModel'
     form = 'myapp.forms.MyForm'
     authorize = generics.only_owner_can_write_except_for_admin

TODO: ``authorize`` メソッドに関する詳細な説明
