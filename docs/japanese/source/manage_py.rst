====================
Kay 管理用スクリプト
====================

概要
----

Kay には ``manage.py`` という管理用のスクリプトが付いています。このスクリプトで、アプリケーション管理タスクの大部分をカバーできます。パラメーター無しで呼出せばヘルプを見る事ができます。

タスクの一部は、Google App Engine SDK が提供するコマンドを実行しますが、実行の際にパラメータの調整や、事前準備を行います。

ですので、GAE 附属のスクリプト( appcfg.py や dev_appserver.py または bulkloader.py )をそのまま使用する事はなるべく避けてください。


.. program:: manage.py add_translation

manage.py add_translation
-------------------------

指定したアプリケーションに新しい言語カタログを追加します。

.. code-block:: bash

  $ python manage.py add_translation [options]

  
.. cmdoption:: -a app_name

   アプリケーション名を指定します。

.. cmdoption:: -l lang

   言語コードを指定します。例) ja

.. cmdoption:: -f

   指定すると、既存のカタログがあっても上書きされます。


.. _appcfg_label:

manage.py appcfg
----------------

このサブコマンドは 素のGAE で appcfg.py にて行うタスクを実行するためのものです。appcfg サブコマンドの使用方法は下記のとおりです:

.. code-block:: bash

  $ python manage.py appcfg [options] <action>

action は下記のどれかである必要があります:

 * cron_info: cron ジョブの情報を表示します。
 * download_data: データストアからデータをダウンロードします。
 * help: あるアクションのヘルプを表示します。
 * request_logs: Apache の common log フォーマットでログを書き出します。
 * rollback: 実行途中のアップデートをロールバックします。
 * update: アプリケーションをアップロードします。
 * update_cron: アプリケーションの cron 設定を更新します。
 * update_indexes: アプリケーションの index を更新します。
 * update_queues: アプリケーションのタスクキュー設定を更新します。
 * upload_data: データストアにデータをアップロードします。
 * vacuum_indexes: アプリケーションで使用しない index を削除します。

``help`` アクションに続いてアクション名を指定する事で、特定のアクションに対するヘルプを表示できます。例えば、下記のように実行すれば ``update`` アクションのヘルプが得られます:

.. code-block:: bash

  $ python manage.py appcfg help update

Kay は引数にカレントディレクトリを自動的に補完します。ですので、各アクションのヘルプにあるようにアプリケーションディレクトリを指定する必要はありません(この動作はちょっと紛らわしいので将来は修正されるかもしれません)。例えばアプリケーションをアップロードするには下記のコマンドでオッケイです:

.. code-block:: bash

  $ python manage.py appcfg update  


現バージョンの Kay は、GAE のサーバ上では事前パースされた jinja2 テンプレートのみ読み込みますので、デプロイの前にテンプレートの事前パースが必要です。manage.py スクリプトは自動的に事前パースを行いますので、普段ユーザーはこの事を気にする必要はありません。もし、MacOSX のランチャーを使っている場合には ``deploy`` ボタンを押すだけでは jinja2 テンプレートの事前パースは行われません。このような場合は、 :ref:`preparse_apps` のようにすればテンプレートの事前パースを行う事ができます。


.. _preparse_apps:

manage.py preparse_apps
-----------------------

このコマンドは、 :attr:`settings.INSTALLED_APPS` の設定値に基いて、全ての jinja2 テンプレートを事前パースします。

.. code-block:: bash

  $ python manage.py preparse_apps


.. program:: manage.py dump_all

manage.py dump_all
------------------

すべてのデータをサーバからダンプします。

.. cmdoption:: --help

   ヘルプを表示します。

.. cmdoption:: -n, --data-set-name string    

   TODO

.. cmdoption:: -i, --app-id string

   ``appid`` を指定します。

.. cmdoption:: -u, --url string

   URLを指定します。

.. cmdoption:: -d, --directory string


.. seealso:: :doc:`dump_restore`



.. program:: manage.py restore_all

manage.py restore_all
---------------------

すべてのデータをサーバにリストアします。

.. cmdoption:: --help
.. cmdoption:: -n, --data-set-name string    
.. cmdoption:: -i, --app-id string    
.. cmdoption:: -u, --url string    
.. cmdoption:: -d, --directory string    


.. seealso:: :doc:`dump_restore`


.. program:: manage.py shell

manage.py shell
---------------

Pythonシェルを起動します。

.. code-block:: bash

  $ python manage.py shell [options]

  
.. cmdoption:: --datastore-path string

   データストアのパスを指定します。

.. cmdoption:: --history-path string

   クエリの履歴ファイルのパスを指定します。

.. cmdoption:: --no-useful-imports

   自動インポートを解除して起動します。アプリケーション配下のモデル定義がインポートされなくなります。

.. cmdoption:: --no-use-ipython
   
   iPythonを使わずに通常の対話型シェルを起動します。
    
.. seealso:: http://code.google.com/intl/ja/appengine/docs/python/tools/devserver.html#The_Development_Console


.. program:: manage.py rshell

manage.py rshell
----------------

運用サーバのデータストアにアクセスする対話型のシェルを起動します。

.. code-block:: bash

  $ python manage.py rshell


.. cmdoption:: -a, --appid string

   ``appid`` を指定します。

.. cmdoption:: -h, --host string    

   TODO

.. cmdoption:: -p, --path string    

   TODO

.. cmdoption:: --no-useful-imports

   自動インポートを解除して起動します。アプリケーション配下のモデル定義がインポートされなくなります。

.. cmdoption:: --no-secure

   TODO

.. cmdoption:: --no-use-ipython

   iPythonを使わずに通常の対話型シェルを起動します。



.. _startapp:

manage.py startapp
------------------

新しいアプリケーションを作成します。

.. code-block:: bash

  $ python manage.py startapp myapp

  
.. _startproject:

manage.py startproject
----------------------

新しいプロジェクトを作成します。

.. code-block:: bash

  $ python manage.py startproject myproject

  
.. cmdoption:: --proj-name string

   プロジェクト名を指定します


.. _runtest:

manage.py runtest
-----------------

テストを実行します。

.. code-block:: bash

  $ python manage.py runtest


.. _preparse_bundle:

manage.py preparse_bundle
--------------------------

Kay自身の Jinja2 テンプレートを事前パースします。TODO

.. code-block:: bash

  $ python manage.py preparse_bundle

  
.. program:: manage.py extract_messages

manage.py extract_messages
--------------------------

国際化対象のメッセージを抽出して、potファイルを生成します。

.. cmdoption:: -t, --target string

TODO

.. cmdoption:: -d, --domain string messages

TODO


.. program:: manage.py update_translations

manage.py update_translations
-----------------------------

翻訳を更新されたpotファイルで更新します。

.. cmdoption:: -t, --target string    

.. cmdoption:: -l, --lang string    

.. cmdoption:: -s, --statistics


.. program:: manage.py compile_translations

manage.py compile_translations
------------------------------

特定のアプリケーションの全てのテンプレートをコンパイルします。

.. cmdoption:: -a, --app string    


.. program:: manage.py runserver

manage.py runserver
-------------------

dev_appserverを適切なパラメータで起動します。

.. code-block:: bash

  $ python manage.py runserver

.. cmdoption:: --help

ヘルプを表示します

.. seealso:: http://code.google.com/intl/ja/appengine/docs/python/tools/devserver.html#The_Development_Console


.. program:: manage.py bulkloader

manage.py bulkloader
--------------------

適切なパラメータでバルクローダ・スクリプトを実行します。For more

.. code-block:: bash

  $ python manage.py bulkloader

.. cmdoption:: --help

ヘルプを表示します

.. seealso:: http://code.google.com/intl/ja/appengine/docs/python/tools/uploadingdata.html



.. program:: manage.py clear_datastore

manage.py clear_datastore
-------------------------

リモートAPIを使用して、App Engine上のデータを全て消去します。

.. cmdoption:: -a, --appid string    
.. cmdoption:: -h, --host string    
.. cmdoption:: -p, --path string    
.. cmdoption:: -k, --kinds string    
.. cmdoption:: -c, --clear-memcache
.. cmdoption:: --no-secure

.. seealso:: :doc:`dump_restore`



.. program:: manage.py create_user

manage.py create_user
---------------------

リモートAPIを使用して、ユーザを新規作成します。

.. cmdoption:: -u, --user-name string    
.. cmdoption:: -P, --password string
.. cmdoption:: -A, --is-admin
.. cmdoption:: -a, --appid string
.. cmdoption:: -h, --host string
.. cmdoption:: -p, --path string
.. cmdoption:: --no-secure



.. program:: manage.py test

manage.py test
--------------

インストールされたアプリケーションのテストを実行します

.. cmdoption:: --target string    

.. cmdoption:: -v, --verbosity integer 0



.. _wxadmin:

manage.py wxadmin
-----------------

TODO
      
