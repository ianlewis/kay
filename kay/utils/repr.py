# -*- coding: utf-8 -*-

"""
kay.utils.repr
~~~~~~~~~~~~~~~~~~~

This module implements object representations for debugging purposes.
Unlike the default repr these reprs expose a lot more information and
produce HTML instead of ASCII.

Together with the CSS and JavaScript files of the debugger this gives
a colorful and more compact output.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:copyright: (c) 2009 by the Werkzeug Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import sys
import re
from traceback import format_exception_only
try:
  from collections import deque
except ImportError:
  deque = None

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
RegexType = type(_paragraph_re)
_password_re = re.compile(r'passwo?r?d', re.I)
_acsid_re = re.compile(r'acsid', re.I)


def dump(obj=None):
  """Print the object details to stdout._write (for the interactive
  console of the web debugger.
  """
  gen = DebugReprGenerator()
  if obj is None:
    rv = u''
  else:
    rv = gen.dump_object(obj)
  return rv

def _add_subclass_info(inner, obj, base):
  if isinstance(base, tuple):
    for base in base:
      if type(obj) is base:
        return inner
  elif type(obj) is base:
    return inner
  module = ''
  if obj.__class__.__module__ not in ('__builtin__', 'exceptions'):
    module = '%s.' % obj.__class__.__module__
  return '%s%s(%s)' % (module, obj.__class__.__name__, inner)



class DebugReprGenerator(object):

  def __init__(self):
    self._stack = []

  def _sequence_repr_maker(left, right, base=object(), limit=8):
    def proxy(self, obj, recursive):
      if recursive:
        return _add_subclass_info(left + '...' + right, obj, base)
      buf = [left]
      have_extended_section = False
      for idx, item in enumerate(obj):
        if idx:
          buf.append(', ')
        buf.append(self.repr(item))
      buf.append(right)
      return _add_subclass_info(u''.join(buf), obj, base)
    return proxy

  list_repr = _sequence_repr_maker('[', ']', list)
  tuple_repr = _sequence_repr_maker('(', ')', tuple)
  set_repr = _sequence_repr_maker('set([', '])', set)
  frozenset_repr = _sequence_repr_maker('frozenset([', '])', frozenset)
  if deque is not None:
    deque_repr = _sequence_repr_maker('collections.'
                                      'deque([', '])', deque)
  del _sequence_repr_maker

  def regex_repr(self, obj):
    pattern = repr(obj.pattern).decode('string-escape', 'ignore')
    if pattern[:1] == 'u':
      pattern = 'ur' + pattern[1:]
    else:
      pattern = 'r' + pattern
    return u're.compile(%s)' % pattern

  def string_repr(self, obj, limit=70):
    buf = []
    buf.append(obj)
    return _add_subclass_info(u''.join(buf), obj, (str, unicode))

  def dict_repr(self, d, recursive, limit=5):
    if recursive:
      return _add_subclass_info(u'{...}', d, dict)
    buf = ['{']
    have_extended_section = False
    for idx, (key, value) in enumerate(d.iteritems()):
      if idx:
        buf.append(', ')
      if _password_re.search(key) or _acsid_re.search(key):
        value = ''.join(['x' for c in value])
      buf.append('%s: %s' %
                 (self.repr(key), self.repr(value)))
    buf.append('}')
    return _add_subclass_info(u''.join(buf), d, dict)

  def object_repr(self, obj):
    return u'%s' % repr(obj).decode('utf-8', 'replace')

  def dispatch_repr(self, obj, recursive):
    if isinstance(obj, (int, long, float, complex)):
      return u'%r' % obj
    if isinstance(obj, basestring):
      return self.string_repr(obj)
    if isinstance(obj, RegexType):
      return self.regex_repr(obj)
    if isinstance(obj, list):
      return self.list_repr(obj, recursive)
    if isinstance(obj, tuple):
      return self.tuple_repr(obj, recursive)
    if isinstance(obj, set):
      return self.set_repr(obj, recursive)
    if isinstance(obj, frozenset):
      return self.frozenset_repr(obj, recursive)
    if isinstance(obj, dict):
      return self.dict_repr(obj, recursive)
    if deque is not None and isinstance(obj, deque):
      return self.deque_repr(obj, recursive)
    return self.object_repr(obj)

  def fallback_repr(self):
    try:
      info = ''.join(format_exception_only(*sys.exc_info()[:2]))
    except Exception:
      info = '?'
    return u'broken repr (%s)' % \
        info.decode('utf-8', 'ignore').strip()

  def repr(self, obj):
    recursive = False
    for item in self._stack:
      if item is obj:
        recursive = True
        break
    self._stack.append(obj)
    try:
      try:
        return self.dispatch_repr(obj, recursive)
      except Exception:
        return self.fallback_repr()
    finally:
      self._stack.pop()

  def dump_object(self, obj):
    repr = items = None
    if isinstance(obj, dict):
      title = 'Contents of'
      items = []
      for key, value in obj.iteritems():
        if not isinstance(key, basestring):
          items = None
          break
        items.append((key, self.repr(value)))
    if items is None:
      items = []
      repr = self.repr(obj)
      for key in dir(obj):
        if key.startswith("_"):
          continue
        try:
          items.append((key, self.repr(getattr(obj, key))))
        except Exception:
          pass
      title = 'Details for'
    title += ' ' + object.__repr__(obj)[1:-1]
    return "%s\n%s\n%s\n" % \
        (title, repr,
         "\n".join(["%s: %s" % (key, v) for (key, v) in items]))
