"""
Kay jinja2 extesions.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging
try:
  from hashlib import sha1
except ImportError:
  from sha import new as sha1

from google.appengine.api import memcache
from jinja2 import nodes
from jinja2.ext import Extension

from kay.utils import local

class FragmentCacheExtension(Extension):
  # a set of names that trigger the extension.
  tags = set(['cache'])

  def __init__(self, environment):
    super(FragmentCacheExtension, self).__init__(environment)

    # add the defaults to the environment
    environment.extend(
      fragment_cache_ns='fragment_cache',
    )

  def parse(self, parser):
    # the first token is the token that started the tag.  In our case
    # we only listen to ``'cache'`` so this will be a name token with
    # `cache` as value.  We get the line number so that we can give
    # that line number to the nodes we create by hand.
    lineno = parser.stream.next().lineno

    # now we parse a single expression that is used as cache key.
    args = [parser.parse_expression()]

    # if there is a comma, the user provided a timeout.  If not use
    # None as second parameter.
    if parser.stream.skip_if('comma'):
      args.append(parser.parse_expression())
    else:
      args.append(nodes.Const(None))
    
    if parser.stream.skip_if('comma'):
      vary_on = parser.parse_tuple()
    else:
      vary_on = (nodes.Const(None))
    args.append(vary_on)

    # now we parse the body of the cache block up to `endcache` and
    # drop the needle (which would always be `endcache` in that case)
    body = parser.parse_statements(['name:endcache'], drop_needle=True)

    # now return a `CallBlock` node that calls our _cache_support
    # helper method on this extension.
    return nodes.CallBlock(self.call_method('_cache_support', args),
                           [], [], body).set_lineno(lineno)

  def _cache_support(self, name, timeout, vary_on, caller):
    """Helper callback."""
    key_seeds = [name, local.request.lang]
    if vary_on is not None:
      if isinstance(vary_on, tuple):
        for v in vary_on:
          key_seeds.append(str(v))
      else:
        key_seeds.append(str(vary_on))
    key = sha1('|'.join(key_seeds).encode('utf-8')).hexdigest()
    # try to load the block from the cache
    # if there is no fragment in the cache, render it and store
    # it in the cache.
    rv = memcache.get(key, namespace=self.environment.fragment_cache_ns)
    if rv is not None:
      logging.debug('Fragment cache hit: key "%s".' % key)
      return rv
    rv = caller()
    memcache.set(key, rv, timeout,
                 namespace=self.environment.fragment_cache_ns)
    logging.debug('Fragment cache set: key "%s".' % key)
    return rv

fragmentcache=FragmentCacheExtension
