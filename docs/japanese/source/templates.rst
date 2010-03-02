=================
Jinja2 を使用する
=================

概要
----

Kay では HTML のレンダリングに Jinja2 を使用しています。Kay は 拡張やフィルターのロードや、Jinja2 の環境設定を行います。また Kay は アプリケーションのデプロイ前に、自動でテンプレートをコンパイルして Python コードにしておきます。これにより、テンプレートに初回アクセスした時の、レンダリングスピードが速くなります。


テンプレートの書き方
--------------------

テンプレートの書き方については、 `Jinja2 Template Designer Documentation <http://jinja.pocoo.org/2/documentation/templates>`_ を参照してください。
  

Context Processors
------------------

Django の context processors と同じように、Kay ではテンプレートのレンダリング時に共通して使用するデータを提供する関数を定義しておく事ができます。

個々の context processor は ``request`` object を引数に取る python callable で、テンプレートの context に追加する辞書を返すきまりになっています。辞書の key がテンプレート内でそのデータを使用する際の名前になります。

processor は順番に適用されます。これはある processor が context に追加したデータをその後で定義した processor が上書きする可能性があるという事です。デフォルトで適用される processor は下記のようになっています。

.. currentmodule:: kay.context_processors

.. function:: request()

template context に ``request`` の名前で ``Request`` オブジェクトを追加します。

.. function:: url_functions()

いくつかの便利な url 関係の関数を追加します。(``url_for``, ``reverse``, ``create_login_url``, ``create_logout_url``)

.. function:: i18n()

この processor は現在の言語コードを ``language_code`` という名前で追加します。

.. function:: media_url()

``media_url`` という名前で :attr:`settings.MEDIA_URL` の値を追加します。

テンプレートの読み込み
----------------------

:attr:`settings.TEMPLATE_DIRS` を設定する事で、優先的にテンプレートを読み込むディレクトリを指定できます。プロジェクトのルートからの相対パスを文字列のリスト又はタプルとして設定します。例:

.. code-block:: python

  TEMPLATE_DIRS = (
    'templates/default',
    'templates/other',
  )

この場合、始めに default ディレクトリを見てテンプレートが無ければ other ディレクトリを探索します。

なお ``APP_DIR/templates`` ディレクトリは自動的に読み込みの対象になります。

Extension と Filter
-------------------

Kay では Jinja2 extension が使用できます。どの extension を使用するか :attr:`settings.JINJA2_EXTENSIONS` で設定できます。filter も同じように :attr:`settings.JINJA2_FILTERS` で設定できます。ただこちらは辞書になっていて、key は filter の名前になります。下記は設定の一例です:

.. code-block:: python

  JINJA2_EXTENSIONS = (
    'myapp.jinja2.extensions.my_extension',
  )

  JINJA2_FILTERS = {
    'my_filter': 'myapp.jinja2.filters.do_my_filter',
    'my_other_filter': 'my_other_app2.jinja2.filters.do_my_filter',
  }
