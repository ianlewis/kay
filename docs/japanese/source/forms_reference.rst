=======================================
kay.utils.forms モジュール リファレンス
=======================================

このフォームモジュールは、 http://zine.pocoo.org/ の Zine project から流用したものです。


.. module:: kay.utils.forms

.. class:: Widget

  すべてのウィジェットのベースクラスです。すべてのウィジェットは、テンプレートの内部から使えるように共通のインターフェースをもっています。

  例として、以下のフォームを取り上げてみます。

  >>> class LoginForm(Form):
  ...     username = TextField(required=True)
  ...     password = TextField(widget=PasswordInput)
  ...     flags = MultiChoiceField(choices=[1, 2, 3])
  ...
  >>> form = LoginForm()
  >>> form.validate({'username': '', 'password': '',
  ...                'flags': [1, 3]})
  False
  >>> widget = form.as_widget()

  インデックスでサブウィジェットを取得できます。

  >>> username = widget['username']
  >>> password = widget['password']

  ウィジェットをレンダリングするには、通常 `render()` メソッドを呼び出します。すべてのキーワードパラメータは、生成されたタグの HTML 属性として使われます。ウィジェット自体を呼び出すことも可能です (``username.render()`` のかわりに ``username()`` とする) 。フィールドにエラーがなければ同じように動作します。エラーがあった場合はウィジェットの後にデフォルトのエラーリストを追加します。

  ウィジェットは、パブリックな属性をいくつかもっています。

  `errors`

      エラーのリストを取得できます。

      >>> username.errors
      [u'This field is required.']

      このエラーリストは print できます。

      >>> print username.errors()
      <ul class="errors"><li>This field is required.</li></ul>


      リストを生成する他のシーケンスと同様、 `as_ul` と `as_ol` メソッドを提供しています。

      >>> print username.errors.as_ul()
      <ul><li>This field is required.</li></ul>

	  
	  ``widget.errors()`` と ``widget.errors.as_ul(class_='errors', hide_empty=True)`` が等価であることを覚えておいてください。

  `value`

      ウィジェットの値をプリミティブ型で返します。通常のウィジェットでは常に文字列です。サブウィジェットをもつウィジェットや複数の値をもつウィジェットではディクショナリかリストです。

      >>> username.value
      u''
      >>> widget['flags'].value
      [u'1', u'3']

  `name` ではフォームのフィールド名を取得できます。

      >>> username.name
      'username'

      ネーム はいつも明らかというわけではないということを覚えておいてください。 Zine はネストされたフォームをサポートしているので、常にネーム属性を使うのはいいアイディアです。

  `id`

      ウィジェットのデフォルトドメインを取得できます。フィールドのためのアイディアがない場合は ``None`` で、そうでない場合は `f_` + ドットのかわりにアンダースコアつきのフィールド名となります：

      >>> username.id
      'f_username'

  `all_errors`

      `errors` と同様ですが、サブウィジェットのエラーも含みます。


.. class:: Input(field, name, value, all_errors)

   Bases: :class:`kay.utils.forms.Widget`

   HTML 入力フィールドウィジェット


   
.. class:: FileInput(field, name, value, all_errors)

   Bases: :class:`kay.utils.forms.Input`

   ファイルを保持するウィジェット

   
.. class:: TextInput(field, name, value, all_errors)

   Bases: :class:`kay.utils.forms.Input`

   テキストを保持するウィジェット

   
.. class:: PasswordInput(field, name, value, all_errors)

   Bases: :class:`kay.utils.forms.TextInput`

   パスワードを保持するウィジェット

   
.. class:: HiddenInput(field, name, value, all_errors)

   Bases: :class:`kay.utils.forms.Input`

   隠蔽された入力フィールド

   
.. class:: Textarea(field, name, value, all_errors)

   Bases: :class:`kay.utils.forms.Widget`

   テキストエリアを表示します。

   
.. class:: Checkbox(field, name, value, all_errors)

   Bases: :class:`kay.utils.forms.Widget`

   簡単なチェックボックス

   .. method:: with_help_text(self, **attrs)

   ヘルプテキストをつけてチェックボックスをレンダリングします。

   .. method:: def as_dd(self, **attrs)

   dt/dd 要素を返します。
  
   .. method:: def as_li(self, **attrs)

   li 要素を返します。

   
.. class:: SelectBox(field, name, value, all_errors)
   
   Bases: :class:`kay.utils.forms.Widget`

   セレクトボックス

   
.. class:: RadioButton(field, name, value, all_errors)

   Bases: :class:`kay.utils.forms._InputGroupMember`

   入力グループのラジオボタン

   
.. class:: GroupCheckbox(field, name, value, all_errors)
   
   Bases: :class:`kay.utils.forms._InputGroupMember`

   入力グループのチェックボックス

   
.. class:: RadioButtonGroup(field, name, value, all_errors)
   
   Bases: :class:`kay.utils.forms._InputGroupMember`

   入力グループのラジオボタン   

   
.. class:: CheckboxGroup(field, name, value, all_errors)
   
   Bases: :class:`kay.utils.forms._InputGroupMember`

   入力グループのラジオボタン   
   

.. class:: Field(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`object`

   抽象フィールドベースクラス

   .. method:: apply_validators(self, value)

   値に対してすべてのヴァリデータを適用します。

   .. method:: should_validate(self, value)

   デフォルトでは、値が None ではない場合、ヴァリデートします。このメソッドは、もしフィールドが空で入力必須ではない場合、ヴァリデーションを行わないように用いられるようなカスタムヴァリデータが適用される前に呼ばれます。

   例えば、 `is_valid_ip` のようなヴァリデータは、値が空の文字列であり、かつ、入力必須のフィールドのチェック時にヴァリデーションエラーがあがっていないような場合は、決して呼び出されることはありません。

   .. method:: def convert(self, value)

   サブクラスでオーバーライドされ、値の変換を提供します。

   .. method:: to_primitive(self, value)

   値をプリミティブ型に変換します（文字列、リスト、ディクショナリ、文字列のリスト/ディクショナリ）。

   このメソッドは失敗してはいけません！

   .. method:: bound(self)

   フォームがデータに束縛されている場合 ``True`` を返します。

   
.. class:: Multiple(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.Field`

   一連の値に単一のフィールドを適用します。

   >>> field = Multiple(IntegerField())
   >>> field([u'1', u'2', u'3'])
   [1, 2, 3]

   推奨されるウィジェット:

   -   `ListWidget` -- デフォルトです。複合フィールドで使うときに便利です。
   -   `CheckboxGroup` -- 選択と一緒に使うと便利です。
   -   `SelectBoxWidget` -- 選択と一緒に使うと便利です。
  

.. class:: CommaSeparated(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.Multiple`

   複数フィールドと同じように機能しますが、カンマで区切られた値を扱います。

   >>> field = CommaSeparated(IntegerField())
   >>> field(u'1, 2, 3')
   [1, 2, 3]

   デフォルトのウィジェットは、 `TextInput` ですが、 `Textarea` も可能です。
  

.. class:: LineSeparated(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.CommaSeparated`

   `CommaSeparated` と同じように機能しますが、複数行を扱います:

   >>> field = LineSeparated(IntegerField())
   >>> field(u'1\n2\n3')
   [1, 2, 3]

   デフォルトのウィジェットは `Textarea` で、それがこのウィジェットに対しては唯一有意です。

   
.. class:: TextField(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.Field`

   文字列用のフィールド

   >>> field = TextField(required=True, min_length=6)
   >>> field('foo bar')
   u'foo bar'
   >>> field('')
   Traceback (most recent call last):
     ...
   ValidationError: This field is required.

   
.. class:: RegexField(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.TextField`
   
   
.. class:: EmailField(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.RegexField`
   

.. class:: DateTimeField(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.Field`
   
   datetime オブジェクト用のフィールド

   >>> field = DateTimeField()
   >>> field('1970-01-12 00:00')
   datetime.datetime(1970, 1, 12, 0, 0)

   >>> field('foo')
   Traceback (most recent call last):
      ...
   ValidationError: Please enter a valid date.

   
.. class:: ModelField(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.Field`

   モデルにクエリを発行するフィールド

   第１引数はモデルの名前です。もし、キーが与えられていない（ None である）場合、プライマリキーに仮定されます。init または、 set_query() を使えばいつでもクエリパラメータを特定することが可能です。これにより、クエリベースのオプションレンダリングとヴァリデーションが可能になります。

   以下に init の後にクエリを設定する例を示します。

   >>> class FormWithModelField(Form):
   ...    model_field = forms.ModelField(model=TestModel, reuired=True)

   >>> form = FormWithModelField()
   ... query = TestModel.all().filter('user =', user.key())
   ... form.model_field.set_query(query)

   モデルクラスが ``__unicode__()`` メソッドを持つ場合、このメソッドの戻り値はオプションタグにおいて、テキストのレンダリングに使われます。 ``__unicode__()`` メソッドがない場合は、 ``Model.__repr__()`` が、この目的に使われます。このフィールドの初期化時に ``option_name`` キーワード引数とともに、オブションタグの値を名前に持つ属性を渡せば、この振る舞いをオーバーライドできます。
  
   .. method:: set_query(self, query)

   このメソッドで直接クエリをセットできます。

   
.. class:: HiddenModelField(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.ModelField`

   プライマリキーによって識別されたモデルを指す隠蔽フィールド。フォームを経由して、モデルに渡すことができます。
   

.. class:: ChoiceField(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.Field`

   多数の選択肢からひとつをユーザに選ばせるフィールド

   選択フィールドは、正しい値であれば複数選択を許容します。値は unicode に変換された後、比較されます。以下のようになります。
   ``1 == "1"``:

   >>> field = ChoiceField(choices=[1, 2, 3])
   >>> field('1')
   1
   >>> field('42')
   Traceback (most recent call last):
     ...
   ValidationError: Please enter a valid choice.

   ``a == b`` であるか、または、`primitive`が値のプリミティブとなっていて ``primitive(a) == primitive(b)`` である場合、`a` と `b` の２つの値は等しいと考えられます。プリミティブは、以下のアルゴリズムによって作成されます。

       1.  もしオブジェクトが `None` であれば、プリミティブは空の文字列となる。
       2.  それ以外の場合、プリミティブはオブジェクトの文字列値となる。

   選択フィールドは、タプルのリストも許容します。最初の要素が比較に使われ、２番目の要素は表示に使われます。 `SelectBoxWidget` だと以下のようになります。

   >>> field = ChoiceField(choices=[(0, 'inactive'), (1, 'active')])
   >>> field('0')
   0

   フィールドは全てヴァリデーションの前にフォームに束縛されるので、後で選択することも可能です。

   >>> class MyForm(Form):
   ...     status = ChoiceField()
   ...
   >>> form = MyForm()
   >>> form.status.choices = [(0, 'inactive', 1, 'active')]
   >>> form.validate({'status': '0'})
   True
   >>> form.data
   {'status': 0}

   もし選択フィールドが "not required" とセットされていて、 `SelectBox` がウィジェットとして使われている場合、未選択を提供するか、フィールドを空のままにできないようにしなければなりません。

   >>> field = ChoiceField(required=False, choices=[('', _('Nothing')),
   ...                                              ('1', _('Something'))])
  

.. class:: MultiChoiceField(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)

   Bases: :class:`kay.utils.form.ChoiceField`

   ユーザに複数の選択肢を用意するフィールド

   
.. class:: NumberField(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.Field`

   >>> field = IntegerField(min_value=0, max_value=99)
   >>> field('13')
   13

   >>> field('thirteen')
   Traceback (most recent call last):
     ...
   ValidationError: Please enter a whole number.

   >>> field('193')
   Traceback (most recent call last):
     ...
   ValidationError: Ensure this value is less than or equal to 99.

   
.. class:: IntegerField(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.NumberField`

   整数値用のフィールド

   >>> field = IntegerField(min_value=0, max_value=99)
   >>> field('13')
   13

   >>> field('thirteen')
   Traceback (most recent call last):
     ...
   ValidationError: Please enter a whole number.

   >>> field('193')
   Traceback (most recent call last):
     ...
   ValidationError: Ensure this value is less than or equal to 99.

   
.. class:: FloatField(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.NumberField`

   フロート値用のフィールド

   >>> field = IntegerField(min_value=0, max_value=99)
   >>> field('13.4')
   13.4

   >>> field('thirteen')
   Traceback (most recent call last):
     ...
   ValidationError: Please enter a float number.

   >>> field('193.2')
   Traceback (most recent call last):
     ...
   ValidationError: Ensure this value is less than or equal to 99.
  

.. class:: FileField(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.Field`

   ファイルアップロード用のフィールド
  

.. class:: BooleanField(label=None, help_text=None, validators=None, widget=None, messages=None, default=no default)
   
   Bases: :class:`kay.utils.form.Field`

   ブール値用のフィールド

   >>> field = BooleanField()
   >>> field('1')
   True

   >>> field = BooleanField()
   >>> field('')
   False
  

.. class:: Form(initial=None)
   
   フォームのベースクラス

   >>> class PersonForm(Form):
   ...     name = TextField(required=True)
   ...     age = IntegerField()

   >>> form = PersonForm()
   >>> form.validate({'name': 'johnny', 'age': '42'})
   True
   >>> form.data['name']
   u'johnny'
   >>> form.data['age']
   42

   簡単なヴァリデーションエラーを起こしてみましょう。

   >>> form = PersonForm()
   >>> form.validate({'name': '', 'age': 'fourty-two'})
   False
   >>> print form.errors['age'][0]
   Please enter a whole number.
   >>> print form.errors['name'][0]
   This field is required.

   フィールドに対するカスタムヴァリデーションルーティンを追加するには、 ``validate_`` + フィールド名という名前で、引数に value をとるメソッドを追加します。例：

   >>> class PersonForm(Form):
   ...     name = TextField(required=True)
   ...     age = IntegerField()
   ...
   ...     def validate_name(self, value):
   ...         if not value.isalpha():
   ...             raise ValidationError(u'The value must only contain letters')

   >>> form = PersonForm()
   >>> form.validate({'name': 'mr.t', 'age': '42'})
   False
   >>> form.errors
   {'name': [u'The value must only contain letters']}

   他のフィールドと照らし合わせるヴァリデートも可能です。そのヴァリデーションが実行されるのは、他のヴァリデーションをすべて実行した後です。すべてのフィールドのディクショナリを引数にとる ``context_validate`` というメソッドを追加します。
   
   >>> class RegisterForm(Form):
   ...     username = TextField(required=True)
   ...     password = TextField(required=True)
   ...     password_again = TextField(required=True)
   ...
   ...     def context_validate(self, data):
   ...         if data['password'] != data['password_again']:
   ...             raise ValidationError(u'The two passwords must be the same')

   >>> form = RegisterForm()
   >>> form.validate({'username': 'admin', 'password': 'blah', 'password_again': 'blag'})
   False
   >>> form.errors
   {None: [u'The two passwords must be the same']}

   フォームは他のフォームのフィールドとして使うことができます。フォームのフォームフィールドを作成するには、 `as_field` クラスメソッドを呼びます。

   >>> field = RegisterForm.as_field()

   このフィールドは、他のフィールドクラスと同じように扱われます。フィールドとしてのフォームにおいて重要なことは、もしそのフィールドがフォームから使われている場合、ヴァリデータが `form` / `self` として渡された `RegisterForm` のインスタンスではなく、使われている場所のフォームを取得することです。

   フォームフィールドは、フォームのインスタンス化においてフォームに束縛されます。これにより、フォームの特定のインスタンスを変更することが可能になります。例えば、フォームのインスタンスを作成し、 ``del form.fields['name']`` を使って、いくつかのフィールドをなくしたり、選択フィールドの選択内容を変更することもできます。しかし、新しいフィールドは束縛されていないので、インスタンスに追加するのは容易ではありません。直接フォームに保存されたフィールドは通常の属性のように名前でアクセスすることが可能です。

   例：

   >>> class StatusForm(Form):
   ...     status = ChoiceField()
   ...
   >>> StatusForm.status.bound
   False
   >>> form = StatusForm()
   >>> form.status.bound
   True
   >>> form.status.choices = [u'happy', u'unhappy']
   >>> form.validate({'status': u'happy'})
   True
   >>> form['status']
   u'happy'

   フィールドはデフォルト値をサポートしていますが、それほど便利ではありません。このデフォルト値は外部ハンドリングのための注釈にすぎません。フォームヴァリデーションシステムはこれらの値を考慮しません。

   以下は、コンフィギュレーションシステムでの使用例です。

   例:

   >>> field = TextField(default=u'foo')
  

   .. method:: as_widget(self)

   フォームをウィジェットとして返します。

   .. method:: csrf_token(self)

   このフォームのための、ユニークなクロスサイトリクエストフォージェリのセキュリティトークン

   .. method:: is_valid(self)

   フォームが有効なら True を返します。

   .. method:: has_changed(self)

   フォームが変更されたら True を返します。

   .. method:: reset(self)

   フォームをリセットします。

   .. method:: validate(self, data, files=None)

   渡されたデータとフォームを突き合わせて有効かどうかを確認します。

   
