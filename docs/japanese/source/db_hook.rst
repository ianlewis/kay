======================
db_hook 機能を使用する
======================

.. note::

   この機能はまだベータ版です。将来的に実装が変わる可能性があります。

概要
====

Appengine 自体にも `RPC hook の仕組み
<http://code.google.com/intl/ja/appengine/articles/hooks.html>`_ が用意
されています。しかし、この方法ではフックの関数が受け取るのは低レベルの
request/response オブジェクトですので、そういう関数を書くのは少しやっか
いな仕事になってしまいます。

Kay ではもっと簡単にこのフック機能を使用する事ができます。
``kay.utils.db_hook`` パッケージにはユーザーが定義した関数を apiproxy
フックへ登録するための関数が用意されています。

関数
----

.. module:: kay.utils.db_hook

.. function:: register_pre_save_hook(func, model)

   ``func`` を apiproxy の PreCallHooks へ間接的に登録します。この関数
   は指定したモデルのエンティティが保存される前に呼び出されます。

.. function:: register_post_save_hook(func, model)

   ``func`` を apiproxy の PostCallHooks へ間接的に登録します。この関数
   は指定したモデルのエンティティが保存された後に呼び出されます。

これらの登録用関数には、下記のシグネチャーを持つ関数を渡せます:

.. code-block:: python

   def your_hook_function(entity, put_type_id):
     # do something with the entity
     # put_type_id is defined in kay.utils.db_hook.put_type

put_type_id はこのエンティティが新しく作られる(た)物かどうかを推測した
結果を示します。この値は ``kay.utils.db_hook.put_type`` モジュールに定
義されています。

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

私の知る限り、同じ key にて保存されているエンティティがあるかどうかを調
べる事無く、低レベルの request/response オブジェクトだけから、エンティ
ティが新規作成されたのか更新されたのかをきちんと判断する事は不可能です。
そこでこの実装では、多くの場合、エンティティが作成・更新された時間によ
り、そのエンティティが新規作成される(た)のか更新される(た)のかを推測し
ています。

pre_save_hook の中で db.get(entity.key()) を呼び出してエンティティの存
在をチェックすれば、そのエンティティが新規作成なのか更新されるのかが判
定できます。

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

   ``func`` を apiproxy の PreCallHooks へ間接的に登録します。この関数
   は指定したモデルのエンティティが削除される前に呼び出されます。

delete フックに対しては下記のシグネチャーを持つ関数を渡せます:

.. code-block:: python

   def your_hook_function(key):
     # do something with the key
