==================
フォームの使用方法
==================

概要
----

Kay にはフォームを扱うためのユーティリティが付属しています。
``kay.utils.forms`` と ``kay.utils.forms.modelform`` です。Kay のフォームユーティリティを理解する助けとなる概念を説明しておきます。


* Widget

  フィールドやフォーム自体の HTML 表現を担当するクラスです。例えば <input type="text"> や <textarea> または <form>...</form> といったように。HTML のレンダリング担当です。

* Field

  ポストされた値のヴァリデーション担当です。例えば ``FloatField`` はデータがきちんと浮動小数点数である事を保証してくれます。

* Form

  フィールドが集まって出来ていて、自分自身のヴァリデート方法を知っています。また自分自身を Widget に変換する方法も知っています。


初めてのフォーム
----------------

``お問い合わせ`` 機能を実装するためのフォームを考えてみましょう。

.. code-block:: python

  from kay.utils import forms

  class ContactForm(forms.Form):
    subject = forms.TextField(required=True, max_length=100)
    message = forms.TextField(required=True)
    sender = forms.EmailField(required=True)
    cc_myself = forms.BooleanField(required=False)

フォームはフィールドオブジェクトで構成されます。この場合は、フォームには四つのフィールドがあります: ``subject`` ``message`` ``sender`` そして ``cc_myself`` です。
``TextField`` ``EmailField`` ``BooleanField`` は使用可能なフィールドのほんの一部です; 完全なリストは :doc:`forms_reference` を参照ください。

もしフォームが AppEngine のデータストア上でモデルをそのまま追加したり更新したりする目的なら ``ModelForm`` を使用する事でモデル定義を繰り返す事なくフォームを定義できます。


ビュー内でフォームを使用する
----------------------------

ビュー内でフォームを使用する基本パターンは下記のようになります:

.. code-block:: python

  def contact(request):
    form = ContactForm()
    if request.method == "POST":
      if form.validate(request.form):
	# process the data
	# ...
	return redirect("/thanks/")
    return render_to_response("myapp/contact.html", {"form": form.as_widget()})

ここでは処理は3パターンに分れます:

1. フォームがサブミットされていない場合は ``ContactForm`` のインスタンスが作成され、その Widget がテンプレートに渡されます。

2. フォームがサブミットされた場合は ``form.validate(request.form)`` によりヴァリデートされます。もしデータが有効なら正常に処理されユーザーは ``/thanks/`` ページへリダイレクトされます。

3. サブミットされたデータが無効の場合は ``form.as_widget()`` により作成されたエラーメッセージを含む Widget がテンプレートに渡されます。


フォームからのデータを処理する
------------------------------

``form.validate()`` が真を返したなら、フォームの投稿をフォームのヴァリデーションルールを満すものとして安全に扱う事ができます。
ここで ``request.form`` を直接使用する事もできますが ``form.data`` を使用するか以下のスタイルでデータにアクセスしましょう: ``form["subject"]`` ``form["message"]`` または ``form["sender"]`` です。これらのデータはヴァリデートされているだけではなく、便宜のため適切な Python の型に変換されています。上記の例では ``cc_myself`` は真偽値になります。同様に ``IntegerField`` や ``FloatField`` は Python の int や float に変換されます。

上記の例において、フォームデータを処理するコードは下記のようになるでしょう:

.. code-block:: python

  if form.validate(request.form):
    recipients = ["info@example.com"]
    if form["cc_myself"]:
      recipients.append(form["sender"])
    from google.appengine.api import mail
    mail.send_mail(sender=form["sender"], to=recipients,
                   subject=form["subject"], body=form["message"])
    return redirect("/thanks/")


テンプレート内でフォームを表示する
----------------------------------

Widget はとても簡単に表示できます。上記の例では ``ContactForm`` を Widget の形式で ``form`` という名前に割り当ててテンプレートに渡しています。以下はシンプルなテンプレートの例です:

.. code-block:: html

  <body>
    {{ form()|safe }}
  </body>

Widget は callable で、call するとレンダーされた HTML form が得られます。結果は既に HTML escape されており ``safe`` フィルターを付加する必要があります。下記のような出力が得られる筈です:

.. code-block:: html

  <form action="" method="post">
    <div style="display: none">
      <input type="hidden" name="_csrf_token" value="c345asdf.........">
    </div>
    <dl>
      <dt><label for="f_subject">Subject</label></dt>
      <dd><input type="text" id="f_subject" value="" name="subject"></dd>
      <dt><label for="f_message">Message</label></dt>
      <dd><input type="text" id="f_message" value="" name="message"></dd>
      <dt><label for="f_sender">Sender</label></dt>
      <dd><input type="text" id="f_sender" value="" name="sender"></dd>
      <dt><label for="f_cc_myself">Cc myself</label></dt>
      <dd><input type="checkbox" id="f_cc_myself" name="cc_myself"></dd>
    </dl>
    <div class="actions"><input type="submit" value="submit"></div>
  </form>

フォーム表示のカスタマイズ
--------------------------

デフォルトで生成される HTML が気に入らない場合は、jinja2 の ``call`` タグを使用する事で見た目をとことんカスタマイズできます。
``call`` タグを使用する場合には、フォームの中身を(サブミット用のボタンも) ``{% call form() %}`` と ``{% endcall %}`` の間に配置する必要があります。フォーム表示のカスタマイズ方法を見てみましょう:

.. code-block:: html

  <body>
  {% call form() %}
    <div class="fieldWrapper">
      {{ form.subject.label(class_="myLabel")|safe }}
      {{ form.subject()|safe }}
    </div>
    <div class="fieldWrapper">
      {{ form.message.errors()|safe }}
      {{ form.message.label()|safe }}
      {{ form.message.render()|safe }}
    </div>
    <div class="fieldWrapper">
      {{ form.sender.label()|safe }}
      {{ form.sender.render()|safe }}
      {% if form.message.errors %}
	<span class="errors">
	  {% for error in form.message.errors %}
	    {{ error }}&nbsp;
	  {% endfor %}
	</span>
      {% endif %}
    </div>
    <div class="fieldWrapper">
      {{ form.cc_myself.label()|safe }}
      {{ form.cc_myself.render()|safe }}
      {{ form.cc_myself.errors(class_="myErrors")|safe }}
    </div>
    {{ form.default_actions()|safe }}
  {% endcall %}
  </body>

上記の例では、それぞれ違う四つの方法でフィールド Widget を描画しています。個々のフィールドは root Widget の attribute としてアクセスできます。順番に見ていきましょう。

1. 一番目の例

.. code-block:: html

    <div class="fieldWrapper">
      {{ form.subject.label(class_="myLabel")|safe }}
      {{ form.subject()|safe }}
    </div>

このコードは ``subject`` フィールドのラベルを ``myLabel`` class として描画します。
``class`` という単語は予約語なので、アンダースコアを付加する事になっています。
``subject`` フィールド Widget も callable で、call すると input フィールドとエラーメッセージの両方を同時に表す HTML が得られます。

2. 二番目の例

.. code-block:: html

    <div class="fieldWrapper">
      {{ form.message.errors()|safe }}
      {{ form.message.label()|safe }}
      {{ form.message.render()|safe }}
    </div>

二番目の例では、input フィールドとエラーメッセージを別々に描画しています。フィールド Widget を直接 call する代りに ``render()`` メソッドを呼出せば input フィールドのみを表す HTML が得られます。ですので多くの場合、エラーメッセージを表示するコードが別途必要になるでしょう。この例ではエラーメッセージとして下記のような出力が得られます:

.. code-block:: html

  <ul class="errors"><li>This field is required.</li></ul>

``<ul>`` タグがあまり気に入らない場合はどうしたら良いでしょう。

3. 三番目の例

.. code-block:: html

    <div class="fieldWrapper">
      {{ form.sender.label()|safe }}
      {{ form.sender.render()|safe }}
      {% if form.message.errors %}
	<span class="errors">
	  {% for error in form.message.errors %}
	    {{ error }}&nbsp;
	  {% endfor %}
	</span>
      {% endif %}
    </div>

この例ではエラーメッセージをループで処理する方法を示しています。簡単ですので説明は省きます。

4. 四番目の例

.. code-block:: html

    <div class="fieldWrapper">
      {{ form.cc_myself.label()|safe }}
      {{ form.cc_myself.render()|safe }}
      {{ form.cc_myself.errors(class_="myErrors")|safe }}
    </div>

最後の例ではエラーメッセージの描画に class 指定をしています。実際にはレンダーの際にキーワード引数を与える事で、どんな HTML 属性も追加できます。


ファイルアップロード
--------------------

フォームに ``FileField`` かそれを継承したクラスのフィールドがある場合、Widget は自動的に form タグ内の必要な属性を設定します。
``validate()`` メソッドには ``request.form`` だけでなく ``request.files`` を渡す必要があります。ファイルアップロードのやり方を下記に示します:

.. code-block:: python

  # forms.py
  class UploadForm(forms.Form):
    comment = forms.TextField(required=True)
    upload_file = forms.FileField(required=True)

  # views.py
  form = UploadForm()
  if request.method == "POST":
    if form.validate(request.form, request.files):
      # process the data
      # ...
      return redirect("/thanks")


フォームヴァリデーションのカスタマイズ
--------------------------------------

特定のフィールドにヴァリデーション用のメソッドを設定するには、``validate_FIELDNAME`` という形式のメソッドを定義します。例えば ``password`` フィールドのデータが十分安全かどうかを確かめるためには ``validate_password`` メソッドをフォームクラスへ定義します。もしヴァリデーションが失敗したら、適切なエラーメッセージと共に :class:`kay.utils.validators.ValidationError` を発生させる必要があります。

下記に例を示します:

.. code-block:: python

  from kay.utils import forms
  from kay.utils.validators import ValidationError

  class RegisterForm(forms.Form):
    username = forms.TextField(required=True)
    password = forms.TextField(required=True, widget=forms.PasswordInput)

    def validate_password(self, value):
      if not stronger_enough(value):
	raise ValidationError(u"The password you specified is too weak.")

パスワードを確認のため再入力させる場合にはどうしたら良いでしょうか。そのためには ``context_validate`` というメソッドを定義して、複数のフィールドに跨がるデータをチェックする必要があります。例:

.. code-block:: python

  from kay.utils import forms
  from kay.utils.validators import ValidationError

  class RegisterForm(forms.Form):
    username = forms.TextField(required=True)
    password = forms.TextField(required=True, widget=forms.PasswordInput)
    password_confirm = forms.TextField(required=True, widget=forms.PasswordInput)

    def validate_password(self, value):
      if not stronger_enough(value):
	raise ValidationError(u"The password you specified is too weak.")

    def context_validate(self, data):
      if data['password'] != data['password_confirm']:
	raise ValidationError(u"The passwords don't match.")


モデルフォームを使う
--------------------

:class:`kay.utils.forms.modelform.ModelForm` は、特定のモデル定義からフォームを自動生成するのにとても便利なクラスです。

以下のようなモデルがあるとしましょう。

.. code-block:: python

  class Comment(db.Model):
    user = db.ReferenceProperty()
    body = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

上記の定義から、フォームを自動生成することができます。

.. code-block:: python

  from kay.utils.forms.modelform import ModelForm
  from myapp.models import Comment

  class CommentForm(ModelForm):
    class Meta:
      model = Comment
      exclude = ('user', 'created')

``Meta`` という名前でインナークラスを定義すれば、モデルフォームのサブクラスを設定することもできます。 ``Meta`` クラスは以下のクラス属性をもつことができます。

.. class:: Meta

   .. attribute:: model

      参照するモデルクラス

   .. attribute:: fields

   	  フォームに含めるするフィールド名のリスト。 ``fields`` がセットされ、空でなければ、ここに挙げられていないプロパティはフォームから取り除かれ、次の ``exclude`` 属性が無視されます。

   .. attribute:: exclude

      フォームから取り除くフィールド名のリスト

   .. attribute:: help_texts

   	  キーにフィールド名、値にヘルプテキストをもったディクショナリ

作成すると、以下のようにしてフォームを使うことができます。

.. code-block:: python

  from myapp.models import Comment
  from myapp.forms import CommentForm

  def index(request):
    comments = Comment.all().order('-created').fetch(100)
    form = CommentForm()
    if request.method == 'POST':
      if form.validate(request.form):
        if request.user.is_authenticated():
          user = request.user
        else:
          user = None
        new_comment = form.save(user=user)
        return redirect('/')
    return render_to_response('myapp/index.html',
                              {'comments': comments,
                               'form': form.as_widget()})

上記のコードは、このフォームを使って新しいエンティティを保存する際に、フォームで指定されていない値をどうやってエンティティに与えるかを示しています。 ``ModelForm.save`` メソッドは、キーワード引数を受け取り、新しいエンティティのコンストラクタにこれらの引数を渡します。
