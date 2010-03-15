# -*- coding: utf-8 -*-
"""
gaefy.jinja2.compiler
~~~~~~~~~~~~~~~~~~~~~

Helper functions to parse Jinja2 templates and store them as Python code.
The compiled templates can be loaded using gaefy.jinja2.code_loaders,
avoiding all the parsing process.

To compile a whole dir:

  from jinja2 import Environment
  from gaefy.jinja2.compiler import compile_dir

  env = Environment(extensions=['jinja2.ext.i18n'])
  src_path = '/path/to/templates'
  dst_path = '/path/to/templates_compiled'

  compile_dir(env, src_path, dst_path)

:copyright: 2009 by tipfy.org.
:license: BSD, see LICENSE.txt for more details.
"""
import re
import sys
from os import path, listdir, mkdir

def compile_file(env, src_path, dst_path, encoding='utf-8', base_dir=''):
  """Compiles a Jinja2 template to python code.
  Params:
    `env`: a Jinja2 Environment instance.
    `src_path`: path to the source file.
    `dst_path`: path to the destination file.
    `encoding`: template encoding.
    `base_dir`: the base path to be removed from the compiled template
      filename.
  """
  # Read the template file.
  src_file = file(src_path, 'r')
  try:
    source = src_file.read().decode(encoding)
  except Exception, e:
    sys.stderr.write("Failed compiling %s. Perhaps you can check the character"
                     " set of this file.\n" % src_path)
    raise
  src_file.close()

  # Compile the template to raw Python code..
  name = src_path.replace(base_dir, '')
  raw = env.compile(source, name=name, filename=name, raw=True)

  # Save to the destination.
  dst_file = open(dst_path, 'wb')
  dst_file.write(raw)
  dst_file.close()


def compile_dir(env, src_path, dst_path, pattern=r'^[^\.].*\..*[^~]$',
                encoding='utf-8', base_dir=None,
                negative_pattern=r'^.*\.swp$'):
  """Compiles a directory of Jinja2 templates to python code.
  Params:
    `env`: a Jinja2 Environment instance.
    `src_path`: path to the source directory.
    `dst_path`: path to the destination directory.
    `encoding`: template encoding.
    `pattern`: a regular expression to match template file names.
    `base_dir`: the base path to be removed from the compiled template
      filename.
  """
  if base_dir is None:
    # In the first call, store the base dir.
    base_dir = src_path

  for filename in listdir(src_path):
    src_name = path.join(src_path, filename)
    dst_name = path.join(dst_path, filename)

    if path.isdir(src_name):
      if not path.isdir(dst_name):
        mkdir(dst_name)
      compile_dir(env, src_name, dst_name, encoding=encoding,
                  base_dir=base_dir)
    elif path.isfile(src_name) and re.match(pattern, filename) and \
          not re.match(negative_pattern, filename):
      compile_file(env, src_name, dst_name, encoding=encoding,
                   base_dir=base_dir)
