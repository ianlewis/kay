# -*- coding: utf-8 -*-

"""
Kay lazy object for settings.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.

taken from django
"""


class LazyObject(object):
  """
  A wrapper for another class that can be used to delay instantiation
  of the wrapped class.

  This is useful, for example, if the wrapped class needs to use
  Django settings at creation time: we want to permit it to be
  imported without accessing settings.
  """
  def __init__(self):
    self._wrapped = None

  def __getattr__(self, name):
    if self._wrapped is None:
      self._setup()
    if name == "__members__":
      # Used to implement dir(obj)
      return self._wrapped.get_all_members()
    return getattr(self._wrapped, name)

  def __setattr__(self, name, value):
    if name == "_wrapped":
      # Assign to __dict__ to avoid infinite __setattr__ loops.
      self.__dict__["_wrapped"] = value
    else:
      if self._wrapped is None:
        self._setup()
      setattr(self._wrapped, name, value)

  def _setup(self):
    """
    Must be implemented by subclasses to initialise the wrapped object.
    """
    raise NotImplementedError
