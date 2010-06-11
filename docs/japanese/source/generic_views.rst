==================
汎用ビューグループ
==================

.. Note::

  この機能はまだ実験段階です。将来仕様が変わる可能性があります。

CRUD
====

CRUD 概要
---------

``kay.generics.crud.CRUDViewGroup`` を使用すると、汎用的な CRUD の
view を簡単に定義できます。CRUDViewGroup を使用するには、モデル・モデル
フォーム・テンプレートさえあれば良いです。

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

  from kay.generics import crud

  from myapp.forms import MyForm
  from myapp.models import MyModel

  class MyCRUDViewGroup(crud.CRUDViewGroup):
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

  from kay.generics import crud

  class MyCRUDViewGroup(crud.CRUDViewGroup):
    model = 'myapp.models.MyModel'
    form = 'myapp.forms.MyForm'

  view_groups = [MyCRUDViewGroup()]


独自のテンプレートを使用する
----------------------------

``templates`` class attribute を指定すれば、独自のテンプレートが使用で
きます。下記に例を示します:

.. code-block:: python

  class MyCRUDViewGroup(crud.CRUDViewGroup):
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

   class MyCRUDViewGroup(crud.CRUDViewGroup):
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

   from kay.generics import only_owner_can_write_except_for_admin
   from kay.generics import crud


   class MyCRUDViewGroup(crud.CRUDViewGroup):
     model = 'myapp.models.MyModel'
     form = 'myapp.forms.MyForm'
     authorize = only_owner_can_write_except_for_admin

TODO: ``authorize`` メソッドに関する詳細な説明


RESTfull API
============

RESTfull API 概要
-----------------

You can use ``kay.generics.rest.RESTViewGroup`` in order to create
RESTfull APIs easily. You can create various handlers for RESTfull
services of specified models.

Your first REST
---------------

Let's see a simple example.

myapp/models.py:

.. code-block:: python

   # -*- coding: utf-8 -*-
   # myapp.models

   from google.appengine.ext import db

   # Create your models here.

   class MyModel(db.Model):
     comment = db.StringProperty()
     created = db.DateTimeProperty(auto_now_add=True)

Its a simple model for just storing comments. You can create RESTfull
view groups as follows:

myapp/urls.py:

.. code-block:: python

   # -*- coding: utf-8 -*-
   # myapp.urls
   # 

   from kay.routing import (
     ViewGroup, Rule
   )

   from kay.generics.rest import RESTViewGroup

   class MyRESTViewGroup(RESTViewGroup):
     models = ['myapp.models.MyModel']

   view_groups = [
     MyRESTViewGroup(),
     ViewGroup(
       Rule('/', endpoint='index', view='myapp.views.index'),
     )
   ]


This will give you following Method/URL combinations for RESTfull
access to this model, assuming that myapp is mounted at '/'. All the
<typeName> in the example bellow is 'MyModel' in this case.

* GET http://yourdomain.example.com/rest/metadata

  * Gets all known types

* GET http://yourdomain.example.com/rest/metadata/<typeName>

  * Gets the <typeName> type profile (as XML Schema). (If the model is
    an Expando model, the schema will include an "any" element).

* GET http://yourdomain.example.com/rest/<typeName>

  * Gets the first page of <typeName> instances (number returned per
    page is defined by server). The returned list element will contain
    an "offset" attribute. If it has a value, that is the next offset
    to use to retrieve more results. If it is empty, there are no more
    results.

* GET http://yourdomain.example.com/rest/<typeName>?offset=50

  * Gets the page of <typeName> instances starting at offset 50 (0
    based numbering). The offset should generally be filled in from a
    previous request.

* GET http://yourdomain.example.com/rest/<typeName>?<queryTerm>[&<queryTerm>]

  * Gets a page of <typeName> instances using a query filter created
    from the given query terms (with offset features mentioned above).
    Multiple query terms will be AND'ed together to create the filter.
    A query filter term has the structure:
    f<op>_<propertyName>=<value>

    Examples:

    * "feq_author=bob@example.com" means include instances where the
      value of the "author" property is equal to "bob@example.com"

    * "flt_count=37&fin_content=value1,value2" means include instances
      where the value of the "count" property greater than "37" and
      the value of the content property is "value1" or "value2"

    Available operations:

    * ``feq_`` -> "equal to"
    * ``flt_`` -> "less than"
    * ``fgt_`` -> "greater than"
    * ``fle_`` -> "less than or equal to"
    * ``fge_`` -> "greater than or equal to"
    * ``fne_`` -> "not equal to"
    * ``fin_`` -> "in <commaSeparatedList>"
    * ``order=param_name`` will make result set to be ordered

    Blob and Text properties may not be used in a query filter

* GET http://yourdomain.example.com/rest/<typeName>/<key>

  * Gets the single <typeName> instance with the given <key>

* POST http://yourdomain.example.com/rest/<typeName>

  * Create new <typeName> instance using the posted data which should
    adhere to the XML Schema for the type

  * Returns the key of the new instance by default. With "?type=full"
    at the end of the url, returns the entire updated instance like a
    GET request.

* POST http://yourdomain.example.com/rest/<typeName>/<key>

  * Partial update of the existing <typeName> instance with the given
    <key>. Will only modify fields included in the posted xml
    data. (Returns same as previous request)

* PUT http://<service>/rest/<typeName>/<key>

  * Complete replacement of the existing <typeName> instance with the
    given <key>(Returns same as previous request)

* DELETE http://<service>/rest/<typeName>/<key>

  * Delete the existing <typeName> instance

By default, you need to create XML elements as the payload for POST
and PUT requests, but you can also use json payload by setting
"Content-Type" request header to "application/json".

By default, the result set is served in XML format, but you can also
get json response by setting "Accept" request header to
"application/json" as well.


Ajax example
------------

Here is an example for guestbook implementation with using jquery's
ajax request.

myapp/templates/index.html:

.. code-block:: html

   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
   <html>
   <head>
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
   <title>Top Page - myapp</title>
   <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script>
   <script type="text/javascript">
   function deleteEntity(key) {
     $.ajax({
       type: "DELETE",
       url: "/rest/MyModel/"+key,
       success: function(data) {
	 refreshData();
       }
     });
   }
   function displayEntity(entity) {
     $("#comments").append(entity.comment+
       "<i> at " + entity.created + "</i>"+
       '&nbsp;<a href="#" onclick="deleteEntity(\''+entity.key+'\');">x</a><br>');
   }
   function refreshData() {
     $.ajax({
       type: "GET",
       url: "/rest/MyModel?ordering=-created",
       dataType: "json",
       success: function(data) {
	 $("#comments").html("");
	 if (data.list.MyModel) {
	   if (data.list.MyModel.key) {
	     displayEntity(data.list.MyModel);
	   } else {
	     for (var i=0; i < data.list.MyModel.length; i++) {
	       displayEntity(data.list.MyModel[i]);
	     }
	   }
	 }
       }
     });
     $("#comment").focus();
   }
   function sendData() {
     $("#sendButton").attr("disabled", "disabled");
     $.ajax({
       type: "POST",
       url: "/rest/MyModel?type=full",
       dataType: "json",
       contentType: "application/json",
       data: JSON.stringify({"MyModel": {"comment": $("#comment").val()}}),
       success: function(data) {
	 $("#comment").val("");
	 $("#sendButton").attr("disabled", "");
	 refreshData();
       }
     });
   }
   $(document).ready(function(){
     $("#comment").keypress(function(e) {
       if (e.which == 13) {
	 sendData();
       }
     });
     refreshData();
   });
   </script>
   </head>
   <body>
   <input type="text" id="comment">
   <input type="button" onclick="sendData();" value="send" id="sendButton">
   <div id="comments"></div>
   </body>
   </html>
