================
管理用スクリプト
================

概要
----

Kay には ``manage.py`` という管理用のスクリプトが付いています。このスクリプトで、アプリケーション管理タスクの大部分をカバーできます。パラメーター無しで呼出せばヘルプを見る事ができます。

タスクの一部は、Google App Engine SDK が提供するコマンドを実行しますが、実行の際にパラメータの調整や、事前準備を行います。

ですので、GAE 附属のスクリプト( appcfg.py や dev_appserver.py または bulkloader.py )をそのまま使用する事はなるべく避けてください。


.. program:: manage.py add_translations

manage.py add_translations
--------------------------

指定したアプリケーションに新しい言語カタログを追加します。

.. code-block:: bash

  $ python manage.py add_translations [options]

  
.. cmdoption:: -t, --target string

   対象となるディレクトリを指定します。

.. cmdoption:: -a

   指定すると全てのアプリケーションが対象になります。

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



.. program:: manage.py bulkloader

manage.py bulkloader
--------------------

適切なパラメータを指定して、バルクローダ・スクリプトを実行します。

.. code-block:: bash

  $ python manage.py bulkloader [option]

.. cmdoption:: --help

   ヘルプを表示します

.. seealso:: http://code.google.com/intl/ja/appengine/docs/python/tools/uploadingdata.html



.. program:: manage.py clear_datastore

manage.py clear_datastore
-------------------------

リモートAPIを使用して、App Engine上のデータを全て消去します。

.. code-block:: bash

  $ python manage.py clear_datastore

.. cmdoption:: -a, --appid appid

   対象となるアプリケーションを ``appid`` で指定します。指定が無ければ ``app.yaml`` 内の ``application`` に設定された値が使用されます。

.. cmdoption:: -h, --host host

   対象となるアプリケーションをホスト名で指定します。デフォルト値は ``appid.appspot.com`` です。

.. cmdoption:: -p, --path path

   リモートAPIのパスを指定します。デフォルト値は ``/remote_api`` です。

.. cmdoption:: -k, --kinds string    

   削除するエンティティの kind を指定します。kind はデフォルトでは ``appname_model`` となっています。指定が無ければ全てのモデルが対象になります。

.. cmdoption:: -c, --clear-memcache

   memcacheのデータもすべて削除します。

.. cmdoption:: --no-secure

   HTTPSを使用せずに通信します。


.. seealso:: :doc:`dump_restore`



.. program:: manage.py compile_translations

manage.py compile_translations
------------------------------

アプリケーションの全ての国際化カタログをコンパイルします。

.. code-block:: bash

  $ python manage.py compile_translations

.. cmdoption:: -t, --target string

   対象となるディレクトリを指定します。

.. cmdoption:: -a, --all

   指定すると全てのアプリケーションが対象になります。
   

.. program:: manage.py create_user

manage.py create_user
---------------------

リモートAPIを使用して、ユーザを新規作成します。

.. code-block:: bash

  $ python manage.py create_user

.. cmdoption:: -u, --user-name username

   ユーザ名を指定します。

.. cmdoption:: -P, --password password

   パスワードを指定します。

.. cmdoption:: -A, --is-admin

   管理者権限を付与する場合に指定します。

.. cmdoption:: -a, --appid appid

   対象となるアプリケーションを ``appid`` で指定します。デフォルト値は ``settings.py`` の ``APPLICATION_ID`` です。

.. cmdoption:: -h, --host host

   対象となるアプリケーションをホスト名で指定します。デフォルト値は ``appid.appspot.com`` です。

.. cmdoption:: -p, --path path

   リモートAPIのパスを指定します。デフォルト値は ``/remote_api`` です。

.. cmdoption:: --no-secure

   HTTPSを使用せずに通信します。



.. program:: manage.py dump_all

manage.py dump_all
------------------

すべてのデータをサーバからダンプします。

.. cmdoption:: --help

   ヘルプを表示します。

.. cmdoption:: -n, --data-set-name string    

   ``_backup`` 配下に、ここで指定した名称のディレクトリが生成され、データとログファイルが保存されます。

.. cmdoption:: -i, --app-id appid

   データをダンプするアプリケーションを ``appid`` で指定します。

.. cmdoption:: -u, --url url

   データをダンプするアプリケーションをURLで指定します。

.. cmdoption:: -d, --directory directory

   データをダンプするディレクトリを指定します。

.. seealso:: :doc:`dump_restore`



.. program:: manage.py extract_messages

manage.py extract_messages
--------------------------

国際化対象のメッセージを抽出して、potファイルを生成します。

.. code-block:: bash

  $ python manage.py extract_messages [options]

.. cmdoption:: -t, --target directory

   対象となるディレクトリを指定します。

.. cmdoption:: -a, --all

   指定すると全てのアプリケーションが対象になります。

.. cmdoption:: -d, --domain domain

   * ``messages`` を指定すると、Pythonスクリプトと ``templates`` 配下のテンプレートファイルが対象となります。
   * ``jsmessages`` を指定すると、JavaScriptファイルが対象となります。
   

.. _preparse_apps:

manage.py preparse_apps
-----------------------

このコマンドは、 :attr:`settings.INSTALLED_APPS` の設定値に基いて、全ての jinja2 テンプレートを事前パースします。manage.py を使用してアプリケーションをアップロードする時、自動的にこの処理が行われるので、普段は実行する必要はありません。

.. code-block:: bash

  $ python manage.py preparse_apps



.. _preparse_bundle:

manage.py preparse_bundle
--------------------------

Kay自身の Jinja2 テンプレートを事前パースします。Kayの開発者が使用するコマンドです。

.. code-block:: bash

   $ python manage.py preparse_bundle

  

.. program:: manage.py restore_all

manage.py restore_all
---------------------

すべてのデータをサーバにリストアします。

.. code-block:: bash

   $ python manage.py restore_all [options]

.. cmdoption:: --help

   ヘルプを表示します。

.. cmdoption:: -n, --data-set-name datasetname

   ``_backup`` 配下の、ここで指定した名称のディレクトリに保存されているデータをサーバにリストアします。

.. cmdoption:: -i, --app-id appid

   データをリストアするアプリケーションを ``appid`` で指定します。

.. cmdoption:: -u, --url url

   データをリストアするアプリケーションをURLで指定します。

.. cmdoption:: -d, --directory directory

   リストアするデータの保存されたディレクトリを指定します。

.. seealso:: :doc:`dump_restore`



.. program:: manage.py rshell

manage.py rshell
----------------

運用サーバのデータストアにアクセスする対話型のシェルを起動します。

.. code-block:: bash

   $ python manage.py rshell [options]


.. cmdoption:: -a, --appid appid

   ``appid`` を指定します。

.. cmdoption:: -h, --host host    

   対象となるアプリケーションをホスト名で指定します。デフォルト値は ``appid.appspot.com`` です。

.. cmdoption:: -p, --path path

   リモートAPIのパスを指定します。デフォルト値は ``/remote_api`` です。

.. cmdoption:: --no-useful-imports

   自動インポートを解除して起動します。アプリケーション配下のモデル定義がインポートされなくなります。

.. cmdoption:: --no-secure

   HTTPSを使用せずに通信します。

.. cmdoption:: --no-use-ipython

   iPythonを使わずに通常の対話型シェルを起動します。



.. program:: manage.py runserver

manage.py runserver
-------------------

適切なパラメータを指定して、dev_appserverを起動します。


.. code-block:: bash

   $ python manage.py runserver [options]

.. cmdoption:: --help

   ヘルプを表示します

.. seealso:: http://code.google.com/intl/ja/appengine/docs/python/tools/devserver.html#The_Development_Console



.. program:: manage.py shell

manage.py shell
---------------

Pythonの対話型プロンプトを起動します。

.. code-block:: bash

   $ python manage.py shell [options]

  
.. cmdoption:: --datastore-path path

   データストアのパスを指定します。

.. cmdoption:: --history-path path

   クエリの履歴ファイルのパスを指定します。

.. cmdoption:: --no-useful-imports

   自動インポートを解除して起動します。アプリケーション配下のモデル定義がインポートされなくなります。

.. cmdoption:: --no-use-ipython
   
   iPythonを使わずに標準の対話型プロンプトを起動します。
    
.. seealso:: http://code.google.com/intl/ja/appengine/docs/python/tools/devserver.html#The_Development_Console



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

.. cmdoption:: --proj-name projectname

   プロジェクト名を指定します。


   
.. program:: manage.py test

manage.py test
--------------

インストールされたアプリケーションのテストを実行します。

.. code-block:: bash

   $ python manage.py test [options]

.. cmdoption:: --target APP_DIR

   対象となるアプリケーションのディレクトリを指定します。

.. cmdoption:: -v, --verbosity integer

   メッセージの出力レベルを整数で指定します。デフォルト値は ``0`` です。

   * ``0``: 出力なし。
   * ``1``: 進捗を ``.`` で出力。
   * ``2``: テストメソッドの docstring を出力。

   
.. program:: manage.py update_translations

manage.py update_translations
-----------------------------

potファイルで翻訳ファイルを更新します。

.. code-block:: bash

   $ python manage.py update_translations [options]

.. cmdoption:: -t, --target directory

   対象となるディレクトリを指定します。

.. cmdoption:: -a

   指定すると全てのアプリケーションが対象になります。

.. cmdoption:: -l, --lang lang 

   翻訳する言語を指定します。例) -l ja

.. cmdoption:: -s, --statistics

   翻訳の完成度合いを出力します。

