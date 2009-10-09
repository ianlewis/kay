====================
Kay 管理用スクリプト
====================

概要
----

Kay には ``manage.py`` という管理用のスクリプトが付いています。このスクリプトで、アプリケーション管理タスクの大部分をカバーできます。パラメーター無しで呼出せばヘルプを見る事ができます。

タスクの一部は、Google App Engine SDK が提供するコマンドを実行しますが、実行の際にパラメータの調整や、事前準備を行います。

ですので、GAE 附属のスクリプト( appcfg.py や dev_appserver.py または bulkloader.py )をそのまま使用する事はなるべく避けてください。


.. program:: manage.py add_translations

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


.. _dump_all:

manage.py dump_all
------------------

すべてのデータをサーバからダンプします。

.. seealso:: :doc:`dump_restore`

.. _restore_all:

すべてのデータをサーバにリストアします。

.. seealso:: :doc:`dump_restore`

.. _shell:

.. _rshell:

.. _startapp:

.. _startproject:

.. _runtest:

.. _preparse_bundle:

.. _preparse_apps:
済み

.. _extract_messages:

.. _add_translations:
済み

.. _update_translations:

.. _compile_translations:

.. _runserver:



.. code-block:: bash

  $ python manage.py runserver -c


.. _bulkloader:

   http://code.google.com/intl/ja/appengine/docs/python/tools/uploadingdata.html

.. _clear_datastore:

サーバのデータを全て消去します。

.. seealso:: :doc:`dump_restore`

.. _create_user:



.. _wxadmin:


actions:

  bulkloader:
    Execute bulkloader script with appropriate parameters. For more
    details, please invoke 'python manage.py bulkloader --help'.

  clear_datastore:
    Clear all the data on GAE environment using remote_api.
      

    -a, --appid                   string    
    -h, --host                    string    
    -p, --path                    string    
    -k, --kinds                   string    
    -c, --clear-memcache
    --no-secure

  compile_translations:
    Compiling all the templates in specified application.

    -a, --app                     string    

  create_user:
    Create new user using remote_api.
      

    -u, --user-name               string    
    -P, --password                string    
    -A, --is-admin
    -a, --appid                   string    
    -h, --host                    string    
    -p, --path                    string    
    --no-secure

  dump_all:
    undocumented action

    --help
    -n, --data-set-name           string    
    -i, --app-id                  string    
    -u, --url                     string    
    -d, --directory               string    

  extract_messages:
    Extract messages and create pot file.

    -t, --target                  string    
    -d, --domain                  string    messages

  preparse_apps:
    Pre compile all the jinja2 templates in your applications.

  preparse_bundle:
    Pre compile all the jinja2 templates in Kay itself.

  restore_all:
    undocumented action

    --help
    -n, --data-set-name           string    
    -i, --app-id                  string    
    -u, --url                     string    
    -d, --directory               string    

  rshell:
    Start a new interactive python session with RemoteDatastore stub.

    -a, --appid                   string    
    -h, --host                    string    
    -p, --path                    string    
    --no-useful-imports
    --no-secure
    --no-use-ipython

  runserver:
    Execute dev_appserver with appropriate parameters. For more details,
    please invoke 'python manage.py runserver --help'.

  shell:
    Start a new interactive python session.

    --datastore-path              string    
    --history-path                string    
    --no-useful-imports
    --no-use-ipython

  startapp:
    Start new application.

    --app-name                    string    

  startproject:
    Start new application.

    --proj-name                   string    

  test:
    Run test for installed applications.

    --target                      string    
    -v, --verbosity               integer   0

  update_translations:
    Update existing translations with updated pot files.

    -t, --target                  string    
    -l, --lang                    string    
    -s, --statistics

  wxadmin:
    undocumented action
