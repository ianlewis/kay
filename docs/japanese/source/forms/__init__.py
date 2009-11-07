# -*- coding: utf-8 -*-
"""
    kay.utils.forms
    ~~~~~~~~~~~~~~~~

    This module implements a sophisticated form validation and rendering
    system that is based on diva with concepts from django newforms and
    wtforms incorporated.

    It can validate nested structures and works in both ways.  It can also
    handle intelligent backredirects (via :mod:`zine.utils.http`) and supports
    basic CSRF protection.

    For usage informations see :class:`Form`

    :copyright: (c) 2009 by the Zine Team, see AUTHORS for more details.
    :copyright: (c) 2009 by Takashi Matsuo <tmatsuo@candit.jp>
    :license: BSD, see LICENSE for more details.
    This file is originally derived from Zine project.
"""
import re
from datetime import datetime
from unicodedata import normalize
from itertools import chain
from threading import Lock
try:
  from hashlib import sha1
except ImportError:
  from sha import new as sha1

from werkzeug import escape, cached_property, MultiDict
from google.appengine.ext import db

from kay.utils import get_request, url_for
from kay.i18n import _, ngettext, lazy_gettext, parse_datetime, \
     format_system_datetime
#from zine.utils.http import get_redirect_target, _redirect, redirect_to
from kay.utils.crypto import gen_random_identifier
from kay.utils.validators import ValidationError
from kay.utils.datastructures import OrderedDict, missing

class _Renderable(object):
  """Mixin for renderable HTML objects."""

  def render(self):
    pass


class Widget(_Renderable):
  """すべてのウィジェットの基本クラスです。すべてのウィジェットは、テンプレートから使えるように共通のインターフェースをもっています。

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

  ウィジェットをレンダリングするには、通常 `render()` メソッドを呼び出します。すべてのキーワードパラメータは、resulting tag の HTML 属性として使われます。ウィジェット自体を呼び出すことも可能です (``username.render()`` のかわりに ``username()``) 。フィールドにエラーがなければ同じように動作します。エラーがあった場合はウィジェットの後にデフォルトのエラーリストを追加します。TODO

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

      プリミティブとしてウィジェットの値を返します。基本ウィジェットでは常に文字列です。サブウィジェットをもつウィジェットや複数の値をもつウィジェットではディクショナリかリストです。

      >>> username.value
      u''
      >>> widget['flags'].value
      [u'1', u'3']

  `name` ではフォームのフィールド名を取得できます。

      >>> username.name
      'username'

      名称が常に明らかではないということを覚えておいてください。 Zine はネストされたフォームをサポートしているので、常にネーム属性を使うのはいいアイディアです。TODO

  `id`

      ウィジェットのデフォルトドメインを取得できます。これは、フィールドをのアイディアがない場合は ``None`` で、 `f_` + ドットのかわりにアンダースコアつきのフィールド名となります：

      >>> username.id
      'f_username'

  `all_errors`

      `errors` と同様ですが、サブウィジェットのエラーも含みます。
  """

  def __init__(self, field, name, value, all_errors):
    pass
  
  def hidden(self):
    """現在の値に対する見えないフィールドを、ひとつ、または、複数返します。サブウィジェットもハンドリングします。データをそのまま渡す透過フォームに有用です。
    """
    pass
  
  @property
  def localname(self):
    """フィールドのローカル名"""
    pass
  
  @property
  def id(self):
    """ウィジェットの規定のID"""
    pass

  @property
  def value(self):
    """ウィジェットのプリミティブ値"""
    pass

  @property
  def label(self):
    """ウィジェットのラベル"""
    pass

  @property
  def help_text(self):
    """ウィジェットのヘルプテキスト"""
    pass

  @property
  def errors(self):
    """ウィジェットのダイレクトエラー"""
    pass

  @property
  def all_errors(self):
    """現在のエラーとすべての子ウィジェットののエラー"""
    pass

  def as_dd(self, **attrs):
    """dt/dd アイテムを返します"""
    pass


class Label(_Renderable):
  """ラベルを保持します。"""

  def __init__(self, text, linked_to=None):
    pass

  def render(self, **attrs):
    pass


class InternalWidget(Widget):
  """特定のウィジェットは、任意のフォームフィールドでは使えず、他のフィールドに属する特別なウィジェット
  """

class Input(Widget):
  """HTML 入力フィールドウィジェット"""

  def render(self, **attrs):
    pass


class FileInput(Input):
  """ファイルを保持するウィジェット"""
  pass


class TextInput(Input):
  """テキストを保持するウィジェット"""
  pass


class PasswordInput(TextInput):
  """パスワードを保持するウィジェット"""
  pass


class HiddenInput(Input):
  """隠蔽された入力フィールド"""
  pass


class Textarea(Widget):
  """テキストエリアを表示します。"""

class Checkbox(Widget):
  """簡単なチェックボックス"""

  @property
  def checked(self):
    pass

  def with_help_text(self, **attrs):
    """ヘルプテキストをつけてチェックボックスをレンダリングします。"""
    pass

  def as_dd(self, **attrs):
    """dt/dd 要素を返します。"""
    pass
  
  def as_li(self, **attrs):
    """li 要素を返します。"""
    pass

  def render(self, **attrs):
    pass


class SelectBox(Widget):
  """セレクトボックス"""

  def _attr_setdefault(self, attrs):
    pass

  def render(self, **attrs):
    pass

  

class _InputGroupMember(InternalWidget):
  """A widget that is a single radio button."""

  @property
  def name(self):
    pass

  @property
  def id(self):
    pass

  @property
  def checked(self):
    pass

  def render(self, **attrs):
    pass


class RadioButton(_InputGroupMember):
  """入力グループのラジオボタン"""
  pass


class GroupCheckbox(_InputGroupMember):
  """入力グループのチェックボックス"""
  pass


class _InputGroup(Widget):

  def as_ul(self, **attrs):
    """<ul> としてラジオボタンウィジェットをレンダリングします"""
    pass

  def as_ol(self, **attrs):
    """<ol> としてラジオボタンウィジェットをレンダリングします"""
    pass

  def as_table(self, **attrs):
    """<table> としてラジオボタンウィジェットをレンダリングします"""
    pass

  def render(self, **attrs):
    pass


class RadioButtonGroup(_InputGroup):
  """ラジオボタンのグループ"""
  pass

class CheckboxGroup(_InputGroup):
  """チェックボックスのグループ"""


class MappingWidget(Widget):
  """ディクショナリのようなフィールドのための特別なウィジェット"""

  def as_dl(self, **attrs):
    pass


class FormWidget(MappingWidget):
  """フォームウィジェット"""

  def get_hidden_fields(self):
    """このメソッドは、特定の隠蔽フィールド用に、 (key, value) ペアのリストを返すために `hidden_fields` プロパティとして呼び出されます。
    """
    pass

  @property
  def hidden_fields(self):
    """文字列としての隠蔽フィールド"""
    pass

  @property
  def csrf_token(self):
    """テンプレート用に、クロスサイトリクエストフォージェリのチェックトークンを渡します。"""
    pass

  def default_actions(self, **attrs):
    """サブミットボタンつきのデフォルトアクション div を返します。"""
    pass

  def render(self, action='', method='post', **attrs):
    pass

  @property
  def is_multipart(self):
    pass

  def __call__(self, *args, **attrs):
    pass


class ListWidget(Widget):
  """リストのようなフィールドのための特別なウィジェット"""
  pass


class ErrorList(_Renderable, list):
  """エラーを表示するのに使われるクラス"""
  pass


class MultipleValidationErrors(ValidationError):
  """サブフィールドがあげる複数のエラーのための、ヴァリデーションエラーのサブクラス。これは、マッピングとリストフィールドに使われます。
  """

  def unpack(self, key=None):
    rv = {}
    for name, error in self.errors.iteritems():
      rv.update(error.unpack(_make_name(key, name)))
    return rv


class FieldMeta(type):

  def __new__(cls, name, bases, d):
    messages = {}
    for base in reversed(bases):
      if hasattr(base, 'messages'):
        messages.update(base.messages)
    if 'messages' in d:
      messages.update(d['messages'])
    d['messages'] = messages
    return type.__new__(cls, name, bases, d)


class Field(object):
  """抽象フィールド基本クラス"""

  def apply_validators(self, value):
    """値に対してすべてのヴァリデータを適応します。"""
    pass

  def should_validate(self, value):
    """デフォルトでは、値が None ではない場合、ヴァリデートします。このメソッドは、もしフィールドが空で入力必須ではない場合、ヴァリデーションを行わないように用いられるようなカスタムヴァリデータが適用される前に呼ばれます。

    例えば、 `is_valid_ip` のようなヴァリデータは、値が空の文字列で、フィールドが入力必須で、チェック時にヴァリデーションエラーをあげていない場合は、決して呼び出されることはありません。
    """
    pass

  def convert(self, value):
    """サブクラスでオーバーライドされ、値の変換を提供します。
    """
    pass

  def to_primitive(self, value):
    """値をプリミティブに変換します（文字列、または、リストないしディクショナリないし文字列のリスト/ディクショナリ）。

    このメソッドは失敗してはいけません！
    """
    pass

  def get_default(self):
    pass


  @property
  def bound(self):
    """フォームがデータに束縛されている場合 ``True`` を返します。"""
    pass


class Mapping(Field):
  """値のディクショナリにフィールドのセットを適応します。

  >>> field = Mapping(name=TextField(), age=IntegerField())
  >>> field({'name': u'John Doe', 'age': u'42'})
  {'age': 42, 'name': u'John Doe'}

  フィールド構築後ウィジェットに再び束縛することもできますが、 `MappingWidget` がマッピング構造を扱うことのできる唯一の組み込みウィジェットなので、非推奨です。
  """

  def convert(self, value):
    pass

  def to_primitive(self, value):
    pass


class FormMapping(Mapping):
  """マッピングと似ていますが、クロスサイトリクエストフォージェリを防ぎます。"""

  def convert(self, value):
    pass


class FormAsField(Mapping):
  """フォームがフィールドに変換される場合、戻り値となるフィールドオブジェクトはこのクラスのインスタンスとなります。その振る舞いはほとんどの場合、通常の :class:`Mapping` フィールドと同じですが、そこから作成されたフォームクラスを示す :attr:`form_class` を呼ぶ属性であるという違いはあります。
  """

  def __init__(self):
    raise TypeError('can\'t create %r instances' %
                    self.__class__.__name__)


class Multiple(Field):
  """Apply a single field to a sequence of values.

  >>> field = Multiple(IntegerField())
  >>> field([u'1', u'2', u'3'])
  [1, 2, 3]

  Recommended widgets:

  -   `ListWidget` -- the default one and useful if multiple complex
      fields are in use.
  -   `CheckboxGroup` -- useful in combination with choices
  -   `SelectBoxWidget` -- useful in combination with choices
  """

  widget = ListWidget
  messages = dict(too_small=None, too_big=None)
  validate_on_omission = True

  def __init__(self, field, label=None, help_text=None, min_size=None,
               max_size=None, validators=None, widget=None, messages=None,
               default=missing, required=False):
    pass

  @property
  def multiple_choices(self):
    return self.max_size is None or self.max_size > 1

  def convert(self, value):
    pass

  def to_primitive(self, value):
    return map(self.field.to_primitive, _force_list(value))

  def _bind(self, form, memo):
    pass


class CommaSeparated(Multiple):
  """複数フィールドと同じように機能しますが、カンマで区切られた値を扱います。

  >>> field = CommaSeparated(IntegerField())
  >>> field(u'1, 2, 3')
  [1, 2, 3]

  デフォルトのウィジェットは、 `TextInput` ですが、 `Textarea` も可能です。
  """

  widget = TextInput

  def __init__(self, field, label=None, help_text=None, min_size=None,
               max_size=None, sep=u',', validators=None, widget=None,
               messages=None, default=missing, required=False):
    pass

  def convert(self, value):
    pass

  def to_primitive(self, value):
    pass


class LineSeparated(CommaSeparated):
  r"""`CommaSeparated` と同じように機能しますが、複数行を扱います:

  >>> field = LineSeparated(IntegerField())
  >>> field(u'1\n2\n3')
  [1, 2, 3]

  デフォルトのウィジェットは `Textarea` で、それがこのウィジェットに対しては唯一有意です。
  """
  widget = Textarea

  def convert(self, value):
    if isinstance(value, basestring):
      value = filter(None, [x.strip() for x in value.splitlines()])
    return Multiple.convert(self, value)

  def to_primitive(self, value):
    if value is None:
      return u''
    if isinstance(value, basestring):
      return value
    return u'\n'.join(map(self.field.to_primitive, value))


class TextField(Field):
  """文字列用のフィールド

  >>> field = TextField(required=True, min_length=6)
  >>> field('foo bar')
  u'foo bar'
  >>> field('')
  Traceback (most recent call last):
    ...
  ValidationError: This field is required.
  """

  messages = dict(too_short=None, too_long=None)

  def __init__(self, label=None, help_text=None, required=False,
               min_length=None, max_length=None, validators=None,
               widget=None, messages=None, default=missing):
    Field.__init__(self, label, help_text, validators, widget, messages,
                   default)
    self.required = required
    self.min_length = min_length
    self.max_length = max_length

  def convert(self, value):
    pass

  def should_validate(self, value):
    """Validate if the string is not empty."""
    return bool(value)

class RegexField(TextField):
  messages = dict(invalid=lazy_gettext(u"The value is invalid."))
  def __init__(self, regex, *args, **kwargs):
    pass

  def convert(self, value):
    pass

email_re = re.compile(
  r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
  r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'
  r')@(?:[A-Z0-9]+(?:-*[A-Z0-9]+)*\.)+[A-Z]{2,6}$', re.IGNORECASE)

class EmailField(RegexField):
  messages = {
    'invalid': lazy_gettext(u'Enter a valid e-mail address.'),
  }

  def __init__(self, *args, **kwargs):
    RegexField.__init__(self, email_re, *args, **kwargs)


class DateTimeField(Field):
  """datetime オブジェクト用のフィールド

  >>> field = DateTimeField()
  >>> field('1970-01-12 00:00')
  datetime.datetime(1970, 1, 12, 0, 0)

  >>> field('foo')
  Traceback (most recent call last):
    ...
  ValidationError: Please enter a valid date.
  """

  messages = dict(invalid_date=lazy_gettext('Please enter a valid date.'))

  def __init__(self, label=None, help_text=None, required=False,
               rebase=True, validators=None, widget=None, messages=None,
               default=missing):
    Field.__init__(self, label, help_text, validators, widget, messages,
                   default)
    self.required = required
    self.rebase = rebase

  def convert(self, value):
    if isinstance(value, datetime):
      return value
    value = _to_string(value)
    if not value:
      if self.required:
        raise ValidationError(self.messages['required'])
      return None
    try:
      return parse_datetime(value, rebase=self.rebase)
    except ValueError:
      raise ValidationError(self.messages['invalid_date'])

  def to_primitive(self, value):
    if isinstance(value, datetime):
      value = format_system_datetime(value, rebase=self.rebase)
    return value


class ModelField(Field):
  """モデルにクエリを発行するフィールド

  第１引数はモデルの名前です。もし、キーが与えられていない（ None である）場合、プライマリキーに仮定されます。init または、 set_query() を使えばいつでもクエリパラメータを特定することが可能です。これにより、クエリベースのオプションレンダリングとヴァリデーションが可能になります。

  以下に init の後にクエリを設定する例を示します。

  >>> class FormWithModelField(Form):
  ...    model_field = forms.ModelField(model=TestModel, reuired=True)

  >>> form = FormWithModelField()
  ... query = TestModel.all().filter('user =', user.key())
  ... form.model_field.set_query(query)

  モデルクラスが ``__unicode__()`` メソッドを持つ場合、このメソッドの戻り値はオプションタグにおいて、テキストのレンダリングに使われます。 ``__unicode__()`` メソッドがない場合は、 ``Model.__repr__()`` が、この目的に使われます。このフィールドの初期化時に ``option_name`` キーワード引数とともに、オブションタグの値を名前に持つ属性を渡せば、この振る舞いをオーバーライドできます。

  """
  messages = dict(not_found=lazy_gettext(
      u'The selected entity does not exist, or is not allowed to select.'))
  widget = SelectBox

  def convert(self, value):
    pass

  def to_primitive(self, value):
    pass

  def set_query(self, query):
    """このメソッドで直接クエリをセットできます。"""
    pass


class HiddenModelField(ModelField):
  """プライマリキーによって識別されたモデルを指す隠蔽フィールド。フォームを経由して、モデルに渡すことができます。
  """

  def _coerce_value(self, value):
    pass


class ChoiceField(Field):
  """多数の選択肢からひとつをユーザに選ばせるフィールド

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
  """

  widget = SelectBox
  messages = dict(
      invalid_choice=lazy_gettext('Please enter a valid choice.')
  )

  def __init__(self, label=None, help_text=None, required=True,
               choices=None, validators=None, widget=None, messages=None,
               default=missing):
    pass

  def convert(self, value):
    pass

  def _bind(self, form, memo):
    pass


class MultiChoiceField(ChoiceField):
  """ユーザに複数の選択肢を用意するフィールド"""

  multiple_choices = True
  messages = dict(too_small=None, too_big=None)
  validate_on_omission = True

  def __init__(self, label=None, help_text=None, choices=None,
               min_size=None, max_size=None, validators=None,
               widget=None, messages=None, default=missing):
    pass

  def convert(self, value):
    pass

  def to_primitive(self, value):
    return map(unicode, _force_list(value))



class NumberField(Field):
  """数値用のフィールド

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
  """

  messages = dict(
      too_small=None,
      too_big=None,
      value_error=lazy_gettext('Please enter a number.')
  )

  def __init__(self, label=None, help_text=None, required=False,
               min_value=None, max_value=None, validators=None,
               widget=None, messages=None, default=missing):
    Field.__init__(self, label, help_text, validators, widget, messages,
                   default)
    self.required = required
    self.min_value = min_value
    self.max_value = max_value

  def convert(self, value):
    pass

  def _convert(self, value):
    pass


class IntegerField(NumberField):
  """整数値用のフィールド

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
  """
  messages = dict(
      too_small=None,
      too_big=None,
      value_error=lazy_gettext('Please enter a whole number.')
  )
  def _convert(self, value):
    return int(value)


class FloatField(NumberField):
  """フロート値用のフィールド

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
  """
  messages = dict(
      too_small=None,
      too_big=None,
      value_error=lazy_gettext('Please enter a float number.')
  )
  def _convert(self, value):
    return float(value)


class FileField(Field):
  """
  ファイルアップロード用のフィールド
  """
  widget = FileInput
  def __init__(self, label=None, help_text=None, required=False,
               validators=None, widget=None, messages=None, default=missing):
    pass

  def convert(self, value):
    pass

  def to_primitive(self, value):
    # always return None
    return None

class BooleanField(Field):
  """ブール値用のフィールド

  >>> field = BooleanField()
  >>> field('1')
  True

  >>> field = BooleanField()
  >>> field('')
  False
  """

  def __init__(self, label=None, help_text=None, required=False,
               validators=None, widget=None, messages=None, default=missing):
    pass

  def convert(self, value):
    pass

  def to_primitive(self, value):
    pass


class FormMeta(type):
  """フォームのためのメタクラス。フォームの継承を扱い、ヴァリデータ関数を登録します。
  """

  def __new__(cls, name, bases, d):
    pass

  def as_field(cls):
    """このフォームのフィールドオブジェクトを返します。返されたフィールドオブジェクトは、フォームから独立しており、束縛フィールドと同じ方法で更新できます。
    """
    pass

  @property
  def validators(cls):
    return cls._root_field.validators

  @property
  def fields(cls):
    return cls._root_field.fields


class FieldDescriptor(object):

  def __init__(self, name):
    self.name = name

  def __get__(self, obj, type=None):
    pass

  def __set__(self, obj, value):
    pass

  def __delete__(self, obj):
    pass


class Form(object):
  """フォームの基本クラス

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
  >>> form.validate({'username': 'admin', 'password': 'blah',
  ...                'password_again': 'blag'})
  ...
  False
  >>> form.errors
  {None: [u'The two passwords must be the same']}

  フォームは他のフォームのフィールドとして使うことができます。フォームのフォームフィールドを作成するには、 `as_field` クラスメソッドを呼びます。

  >>> field = RegisterForm.as_field()

  このフィールドは、他のフィールドクラスと同じように扱われます。フィールドとしてのフォームにおいて重要なことは、もしそのフィールドがフォームから使われている場合、ヴァリデータが `form` / `self` として渡された `RegisterForm` のインスタンスではなく、使われている場所のフォームを取得することです。TODO

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
  """
#  __metaclass__ = FormMeta


  def as_widget(self):
    """フォームをウィジェットとして返します。"""
    pass

  @property
  def csrf_token(self):
    """このフォームのための、ユニークなクロスサイトリクエストフォージェリのセキュリティトークン"""
    pass

  @property
  def is_valid(self):
    """フォームが有効なら True を返します。"""
    pass

  @property
  def has_changed(self):
    """フォームが変更されたら True を返します。"""
    pass

  @property
  def fields(self):
    pass

  @property
  def validators(self):
    pass

  def reset(self):
    """フォームをリセットします。"""
    pass

  def validate(self, data, files=None):
    """渡されたデータとフォームを突き合わせて有効かどうかを確認します。"""
    pass
