# -*- coding: utf-8 -*-
"""
media_compiler
~~~~~~~~~~~~~~

Compile media files(JavaScript/css)

:Copyright: (c) 2009 reedom, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import copy
import logging
import md5
import os
import re
import shutil
import sys
import tempfile
import types
import yaml

import kay
from kay.conf import settings

import kay.ext.media_compressor.default_settings as media_conf


IS_DEVSERVER = 'SERVER_SOFTWARE' in os.environ and \
    os.environ['SERVER_SOFTWARE'].startswith('Dev')
IS_APPSERVER = 'SERVER_SOFTWARE' in os.environ and \
    os.environ['SERVER_SOFTWARE'].startswith('Google App Engine')

#--------------------------------------------------------------

def union_list(a, b):
  return list(set(a).union(b))

class MediaInfo:
  path_ = os.path.join(kay.PROJECT_DIR, '_media.yaml')

  def __init__(self):
    self.info_ = {}

  @classmethod
  def load(cls):
    instance = cls()
    if os.path.exists(cls.path_):
      istream = open(cls.path_, 'rb')
      try:
        instance.info_ = yaml.safe_load(istream)
      except:
        pass
      finally:
        istream.close()
    return instance

  def save(self):
    ostream = open(self.path_, 'wb')
    try:
      yaml.safe_dump(self.info_, ostream, indent=2)
    finally:
      ostream.close()

  def get(self, category, name):
    info = self.info_.get(category)
    if info is None:
      return None
    return info.get(name)

  def set(self, category, name, new_value):
    info = self.info_.get(category)
    if info is None:
      self.info_[category] = {name: new_value}
    else:
      self.info_[category][name] = new_value

media_info = None

#--------------------------------------------------------------

VERBOSE_SURPRESS = 0
VERBOSE_PRINT = 1
VERBOSE_LOGGING = 2

def surpress_print_status(s):
  pass

print_status_method = surpress_print_status

def print_status(s):
  print_status_method(s)
  
def set_verbose_method(method):
  global print_status_method
  if method == VERBOSE_SURPRESS:
    print_status_method = default_print_status
  elif method == VERBOSE_PRINT:
    print_status_method = kay.management.utils.print_status
  elif method == VERBOSE_LOGGING:
    print_status_method = logging.info

#--------------------------------------------------------------
    
def _merge_css_config(dst, another):
  return _merge_config(dst, another, ['csstidy'])

def _merge_js_config(dst, another):
  return _merge_config(dst, another, ['goog_calcdeps', 'goog_compiler'])

def _merge_config(dst, another, merge_keys):
  if another is None:
    return {} if dst is None else dst
  if getattr(another, 'iteritems', None):
    for k, v in another.iteritems():
      if k in merge_keys and k in dst:
        dst[k].update(v)
      else:
        dst[k] = copy.deepcopy(v)
  return dst

COMPILE_COMMON = copy.deepcopy(media_conf.COMPILE_MEDIA)
COMPILE_COMMON.update(getattr(settings, 'COMPILE_MEDIA_COMMON', {}))
COMPILE_CSS = _merge_css_config(copy.deepcopy(COMPILE_COMMON),
                                media_conf.COMPILE_MEDIA_CSS)
if IS_DEVSERVER:
  COMPILE_CSS = _merge_css_config(COMPILE_CSS,
                                  media_conf.COMPILE_MEDIA_CSS_DEV)
COMPILE_CSS = _merge_css_config(
  COMPILE_CSS, getattr(settings, 'COMPILE_MEDIA_CSS_COMMON', {}))

if IS_DEVSERVER:
  COMPILE_CSS = _merge_css_config(
    COMPILE_CSS, getattr(settings, 'COMPILE_MEDIA_CSS_DEV', {}))

COMPILE_JS = _merge_js_config(copy.deepcopy(COMPILE_COMMON),
                              media_conf.COMPILE_MEDIA_JS)
if IS_DEVSERVER:
  COMPILE_JS = _merge_js_config(COMPILE_JS,
                                media_conf.COMPILE_MEDIA_JS_DEV)
COMPILE_JS = _merge_js_config(
  COMPILE_JS, getattr(settings, 'COMPILE_MEDIA_JS_COMMON', {}))

if IS_DEVSERVER:
  COMPILE_JS = _merge_js_config(
    COMPILE_JS, getattr(settings, 'COMPILE_MEDIA_JS_DEV', {}))

#--------------------------------------------------------------

def manage_static_files():
  if hasattr(settings, 'COMPILE_MEDIA_COMMON') and \
        COMPILE_COMMON.has_key('static_dir') and \
        COMPILE_COMMON['static_dir']:
    _create_symlinks()

def _create_symlinks():
  for from_path, to_path in COMPILE_COMMON['static_dir']:
    src_path = os.path.join(kay.PROJECT_DIR, from_path)
    dest_path = make_output_path_(COMPILE_COMMON, to_path)
    print_status(' %s => %s' % (from_path, dest_path[len(kay.PROJECT_DIR):]))

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
      os.makedirs(dest_dir)
    if not os.path.lexists(dest_path):
      os.symlink(os.path.abspath(from_path), dest_path)

#--------------------------------------------------------------

def get_css_config(tag_name):
  if not getattr(settings, 'COMPILE_MEDIA_CSS'):
    raise Exception('settings.COMPILE_MEDIA_CSS is not defined')
  if not tag_name in settings.COMPILE_MEDIA_CSS:
    raise Exception('settings.COMPILE_MEDIA_CSS["%s"] is not defined' %
                    tag_name)
  return _merge_css_config(copy.deepcopy(COMPILE_CSS), 
                           settings.COMPILE_MEDIA_CSS[tag_name])  

def get_css_urls(tag_name, auto_compile=False):

  css_config = get_css_config(tag_name)
  if not css_config['enabled']:
    if css_config['source_urls']:
      return css_config['source_urls']
    else:
      return [path if re.match(ur'https?://', path) else '/%s' %
              path for path in css_config['source_files']]

  if auto_compile:
    compile_css(tag_name)

  global media_info
  if media_info is None:
    media_info = MediaInfo.load()

  last_info = media_info.get(css_config['subdir'], tag_name)
  if not last_info:
    raise Exception('settings.COMPILE_MEDIA_CSS["%s"] has not been compiled' % 
                    tag_name)
  return last_info['result_urls']

def compile_css(tag_name=None, force=False):
  for name, x in settings.COMPILE_MEDIA_CSS.iteritems():
    if tag_name is not None:
      if tag_name != name:
        continue
    print_status('Compiling css media [%s]' % name)
    css_config = get_css_config(name)
    compile_css_(name, css_config, force)
  return True

def compile_css_(tag_name, css_config, force):
  if IS_APPSERVER:
    return
  
  def needs_update(media_info, output_path):
    if not css_config['enabled']:
      return False
    if not os.path.exists(output_path):
      return True

    last_info = media_info.get(css_config['subdir'], tag_name)
    if not last_info:
      return True
    last_config = last_info.get('config')
    if not last_config:
      return True

    if not equal_object_(last_config, css_config):
      return True

    if 'source_files' not in last_info:
      return True
    for path, mtime in last_info['source_files']:
      if mtime != os.path.getmtime(path):
        return True

  def csstidy(css_path):
    tmp_file = tempfile.NamedTemporaryFile(mode='w+b')
    ifile = open(css_path)
    tmp_file.write(ifile.read())
    ifile.close()
    tmp_file.flush()

    output_file = tempfile.NamedTemporaryFile(mode='w+b')
  
    print_status(" %s %s %s ..." % (css_config['csstidy']['path'],
                                    css_path,
                                    css_config['csstidy']['arguments']))
    command = '%s %s %s %s' % (css_config['csstidy']['path'],
                               tmp_file.name,
                               css_config['csstidy']['arguments'],
                               output_file.name)
    command_output = os.popen(command).read()
  
    filtered_css = output_file.read()
    output_file.close()
    tmp_file.close()
    return filtered_css

  def concat(css_path):
    print_status(" concat %s" % css_path)
    ifile = open(css_path)
    css = ifile.read()
    ifile.close()
    return css

  if css_config['tool'] not in ('csstidy', 'concat'):
    print_status("COMPILE_MEDIA_CSS['tool'] setting is invalid;"
                 " unknown tool `%s'" % css_config['tool'])
    sys.exit(1)

  global media_info
  if media_info is None:
    media_info = MediaInfo.load()

  output_path = make_output_path_(css_config, css_config['subdir'],
                                  css_config['output_filename'])
  if not force and not needs_update(media_info, output_path):
    print_status(' up to date.')
    return

  if css_config['tool'] == 'csstidy':
    tool_method = csstidy
  elif css_config['tool'] == 'concat':
    tool_method = concat

  source_files = []
  for path in css_config['source_files']:
    path = make_input_path_(path)
    logging.info(path)
    source_files.append((path, os.path.getmtime(path)))
  ofile = create_file_(output_path)
  try:
    for path, mtime in source_files:
      ofile.write(tool_method(path))
  finally:
    ofile.close()

  result_url = '/' + make_output_path_(css_config, css_config['subdir'],
                                       css_config['output_filename'],
                                       relative=True)
  last_info = {'config': copy.deepcopy(css_config),
               'source_files': source_files,
               'result_urls': [result_url]}
               
  media_info.set(css_config['subdir'], tag_name, last_info)
  media_info.save()

#--------------------------------------------------------------

def get_js_config(tag_name):
  if not getattr(settings, 'COMPILE_MEDIA_JS'):
    raise Exception('settings.COMPILE_MEDIA_JS is not defined')
  if not tag_name in settings.COMPILE_MEDIA_JS:
    raise Exception('settings.COMPILE_MEDIA_JS["%s"] is not defined' %
                    tag_name)
  return _merge_js_config(copy.deepcopy(COMPILE_JS),
                          settings.COMPILE_MEDIA_JS[tag_name])

def get_js_urls(tag_name, auto_compile=False):
  js_config = get_js_config(tag_name)
  if not js_config['enabled']:
    if js_config['source_urls']:
      return js_config['source_urls']
    else:
      return [path if re.match(ur'https?://', path) else '/%s' %
              path for path in js_config['source_files']]

  if auto_compile:
    compile_js(tag_name)

  global media_info
  if media_info is None:
    media_info = MediaInfo.load()

  last_info = media_info.get(js_config['subdir'], tag_name)
  if not last_info:
    raise Exception('settings.COMPILE_MEDIA_JS["%s"] is not defined' %
                    tag_name)
  return last_info['result_urls']

def compile_js(tag_name = None, force=False):
  for name, x in settings.COMPILE_MEDIA_JS.iteritems():
    if tag_name is not None:
      if tag_name != name:
        continue
    print_status('Compiling js media [%s]' % name)
    js_config = get_js_config(name)
    compile_js_(name, js_config, force)
  return True

def compile_js_(tag_name, js_config, force):
  if IS_APPSERVER:
    return

  def needs_update(media_info):
    if js_config['tool'] != 'goog_calcdeps':
      # update if target file does not exist
      target_path = make_output_path_(js_config, js_config['subdir'],
                                      js_config['output_filename'])
      if not os.path.exists(target_path):
        return True

    # update if it lacks required info in _media.yaml
    last_info = media_info.get(js_config['subdir'], tag_name)
    if not last_info:
      return True
    last_config = last_info.get('config')
    if not last_config:
      return True

    # update if any configuration setting is changed
    if not equal_object_(last_config, js_config):
      return True

    if 'related_files' not in last_info:
      return True
    for path, mtime in last_info['related_files']:
      if mtime != os.path.getmtime(path):
        return True
      
  def jsminify(js_path):
    from StringIO import StringIO
    from kay.ext.media_compressor.jsmin import JavascriptMinify
    ifile = open(js_path)
    outs = StringIO()
    JavascriptMinify().minify(ifile, outs)
    ret = outs.getvalue()
    if len(ret) > 0 and ret[0] == '\n':
      ret = ret[1:]
    return ret

  def concat(js_path):
    print_status(" concat %s" % js_path)
    ifile = open(js_path)
    js = ifile.read()
    ifile.close()
    return js

  def goog_calcdeps():
    deps_config = copy.deepcopy(js_config['goog_common'])
    deps_config.update(js_config['goog_calcdeps'])

    if deps_config.get('method') not in \
          ['separate', 'concat', 'concat_refs', 'compile']:
      print_status("COMPILE_MEDIA_JS['goog_calcdeps']['method'] setting is"
                   " invalid; unknown method `%s'" % deps_config.get('method'))
      sys.exit(1)

    output_urls = []
    if deps_config['method'] == 'separate':
      source_files, output_urls = goog_calcdeps_separate(deps_config)
    elif deps_config['method'] == 'concat':
      source_files, output_urls = goog_calcdeps_concat(deps_config)
    elif deps_config['method'] == 'concat_refs':
      source_files, output_urls = goog_calcdeps_concat_refs(deps_config)
    elif deps_config['method'] == 'compile':
      source_files, output_urls = goog_calcdeps_compile(deps_config)
      source_files = [file[0] for file in source_files]

    related_files = union_list(source_files, 
                               [make_input_path_(path)
                                  for path in js_config['source_files']])
    related_file_info = [(path, os.path.getmtime(path))
                           for path in related_files]
    
    # create yaml info
    last_info = {'config': copy.deepcopy(js_config),
                 'related_files': related_file_info,
                 'result_urls': output_urls}
    media_info.set(js_config['subdir'], tag_name, last_info)
    media_info.save()

  def goog_calcdeps_separate(deps_config):
    source_files = goog_calcdeps_list(deps_config)
    (output_urls, extern_urls) = goog_calcdeps_copy_files(deps_config,
                                                          source_files)
    return (source_files, extern_urls + output_urls)

  def goog_calcdeps_concat(deps_config):
    source_files = goog_calcdeps_list(deps_config)
    (output_urls, extern_urls) = goog_calcdeps_concat_files(deps_config,
                                                            source_files)
    return (source_files, extern_urls + output_urls)

  def goog_calcdeps_concat_refs(deps_config):
    source_files = goog_calcdeps_list(deps_config)
    original_files = [make_input_path_(path)
                      for path in js_config['source_files']]
    ref_files = [path for path in source_files if path not in original_files]
    (output_urls, extern_urls) = goog_calcdeps_concat_files(deps_config,
                                                            ref_files)
    original_urls = [path[len(kay.PROJECT_DIR):] for path in original_files]
    return (source_files, extern_urls + output_urls + original_urls)

  def goog_calcdeps_compile(deps_config):
    comp_config = copy.deepcopy(js_config['goog_common'])
    comp_config.update(js_config['goog_compiler'])

    source_files = []
    extern_urls = []

    command = '%s -o compiled -c "%s" ' % (deps_config['path'],
                                                 comp_config['path'])
    for path in deps_config.get('search_paths', []):
      command += '-p %s ' % make_input_path_(path)
    for path in js_config['source_files']:
      path = make_input_path_(path)
      command += '-i %s ' % path
      source_files.append((path, os.path.getmtime(path)))

    if comp_config['level'] == 'minify':
      level = 'WHITESPACE_ONLY'
    elif comp_config['level'] == 'advanced':
      level = 'ADVANCED_OPTIMIZATIONS'
    else:
      level = 'SIMPLE_OPTIMIZATIONS'
    flags = '--compilation_level=%s' % level
#    for path in comp_config.get('externs', []):
#      flags += '--externs=%s ' % make_input_path_(path)
#    if comp_config.get('externs'):
#      flags += ' --externs=%s ' % " ".join(comp_config['externs'])
    command += '-f "%s" ' % flags
    print_status(command)
    command_output = os.popen(command).read()

    output_path = make_output_path_(js_config, js_config['subdir'],
                                    js_config['output_filename'])
    ofile = create_file_(output_path)
    try:
      for path in comp_config.get('externs', []):
        if re.match(r'^https?://', path):
          extern_urls.append(path)
          continue
        path = make_input_path_(path)
        ifile = open(path)
        try:
          ofile.write(ifile.read())
        finally:
          ifile.close()
        source_files.append((path, os.path.getmtime(path)))
      ofile.write(command_output)
    finally:
      ofile.close()
    return (source_files, extern_urls + [output_path[len(kay.PROJECT_DIR):]])

  def goog_calcdeps_list(deps_config):
    source_files = []

    command = '%s -o list ' % deps_config['path']
    for path in deps_config['search_paths']:
      command += '-p %s ' % make_input_path_(path)
    for path in js_config['source_files']:
      command += '-i %s ' % make_input_path_(path)
    print_status(command)
    command_output = os.popen(command).read()
    for path in command_output.split("\n"):
      if path == '': continue
      source_files.append(path)
    return source_files

  def goog_calcdeps_copy_files(deps_config, source_files):
    extern_urls = []
    output_urls = []

    output_dir_base = make_output_path_(js_config, 'separated_js')

    if not os.path.exists(output_dir_base):
      os.makedirs(output_dir_base)
    if not deps_config.get('use_dependency_file', True):
      output_path = os.path.join(output_dir_base, '__goog_nodeps.js')
      ofile = open(output_path, "w")
      output_urls.append(output_path[len(kay.PROJECT_DIR):])
      try:
        ofile.write('CLOSURE_NO_DEPS = true;')
      finally:
        ofile.close()

    output_dirs = {}
    search_paths = [make_input_path_(path)
                    for path in deps_config['search_paths']]
    for path in search_paths:
      output_dirs[path] = os.path.join(output_dir_base,
                                       md5.new(path).hexdigest())

    all_paths = [make_input_path_(path)
                 for path in deps_config.get('externs', [])]
    all_paths.extend(source_files)
    for path in all_paths:
      if re.match(r'^https?://', path):
        extern_urls.append(path)
        continue

      path = make_input_path_(path)
      output_path = os.path.join(output_dir_base, re.sub('^/', '', path))
      for dir in search_paths:
        if path[0:len(dir)] == dir:
          output_path = os.path.join(output_dirs[dir],
                                     re.sub('^/', '', path[len(dir):]))
          break
      output_dir = os.path.dirname(output_path)

      if not os.path.exists(output_dir):
        os.makedirs(output_dir)
      shutil.copy2(path, output_path)
      output_urls.append(output_path[len(kay.PROJECT_DIR):])
    return (output_urls, extern_urls)
    
  def goog_calcdeps_concat_files(deps_config, source_files):
    extern_urls = []

    output_path = make_output_path_(js_config, js_config['subdir'],
                                    js_config['output_filename'])
    ofile = create_file_(output_path)
    try:
      if not deps_config.get('use_dependency_file', True):
        ofile.write('CLOSURE_NO_DEPS = true;')
      all_paths = [make_input_path_(path)
                   for path in deps_config.get('externs', [])]
      all_paths.extend(source_files)
      for path in all_paths:
        if re.match(r'^https?://', path):
          extern_urls.append(path)
          continue
        ifile = open(make_input_path_(path))
        ofile.write(ifile.read())
        ifile.close()
    finally:
      ofile.close()

    return ([output_path[len(kay.PROJECT_DIR):]], extern_urls)

  selected_tool = js_config['tool']

  if selected_tool not in \
        (None, 'jsminify', 'concat', 'goog_calcdeps', 'goog_compiler'):
    print_status("COMPILE_MEDIA_JS['tool'] setting is invalid;"
                 " unknown tool `%s'" % selected_tool)
    sys.exit(1)

  global media_info
  if media_info is None:
    media_info = MediaInfo.load()

  if not force and not needs_update(media_info):
    print_status(' up to date.')
    return

  if selected_tool == 'goog_calcdeps':
    return goog_calcdeps()

  if selected_tool is None:
    last_info = {'config': copy.deepcopy(js_config),
                 'result_urls': ['/'+f for f in js_config['source_files']]}
    media_info.set(js_config['subdir'], tag_name, last_info)
    media_info.save()
    return

  dest_path = make_output_path_(js_config, js_config['subdir'],
                                js_config['output_filename'])
  ofile = create_file_(dest_path)
  try:
    if selected_tool == 'jsminify':
      for path in js_config['source_files']:
        src_path = make_input_path_(path)
        ofile.write(jsminify(src_path))
    elif selected_tool == 'concat':
      for path in js_config['source_files']:
        src_path = make_input_path_(path)
        ofile.write(concat(src_path))
  finally:
    ofile.close()
  
  if selected_tool == 'goog_compiler':
    comp_config = copy.deepcopy(js_config['goog_common'])
    comp_config.update(js_config['goog_compiler'])
    if comp_config['level'] == 'minify':
      level = 'WHITESPACE_ONLY'
    elif comp_config['level'] == 'advanced':
      level = 'ADVANCED_OPTIMIZATIONS'
    else:
      level = 'SIMPLE_OPTIMIZATIONS'
    command_args = '--compilation_level=%s' % level
    for path in js_config['source_files']:
      command_args += ' --js %s' % make_input_path_(path)
    command_args += ' --js_output_file %s' % dest_path
    command = 'java -jar %s %s' % (comp_config['path'], command_args)
    command_output = os.popen(command).read()

  info = copy.deepcopy(js_config)
  info['output_filename'] = make_output_path_(js_config, js_config['subdir'],
                                              js_config['output_filename'],
                                              relative=True)
  info['result_urls'] = ['/'+info['output_filename']]
  media_info.set(js_config['subdir'], tag_name, info)
  media_info.save()
  
#--------------------------------------------------------------

def make_input_path_(path):
  return os.path.join(kay.PROJECT_DIR, path)

def make_output_path_(config, *path, **kwargs):
  version = config['version']
  if version is not None:
    result = os.path.join(config['output_base_dir'], str(version), *path)
  else:
    result = os.path.join(config['output_base_dir'], *path)

  if kwargs.get('relative'):
    return result
  else:
    return os.path.join(kay.PROJECT_DIR, result)
  
def create_file_(path):
  dirname = os.path.dirname(path)
  if not os.path.exists(dirname):
    os.makedirs(dirname)
  return open(path, 'wb')

def equal_object_(a, b):
  if type(a) == types.DictType and type(b) == types.DictType:
    if len(a.keys()) != len(b.keys()):
      return False
    for k, v in a.iteritems():
      if k not in b:
        return False
      if not equal_object_(v, b[k]):
        return False
    return True
  elif type(a) in [types.ListType, types.TupleType] and \
        type(b) in [types.ListType, types.TupleType]:
    if len(a) != len(b):
      return False
    ia = iter(a)
    ib = iter(b)
    try:
      while True:
        if not equal_object_(ia.next(), ib.next()):
          return False
    except:
      pass
    return True
  else:
    return a == b
