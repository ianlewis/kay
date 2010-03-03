# -*- coding: utf-8 -*-

#--------------------------------------------------------------

# COMPILE_MEDIA_VERSION = 1
# COMPILE_MEDIA_BASE_DIR = '_generated_media'
# 
# COMPILE_MEDIA_STATIC = (
#   ('media/images', 'images'),
#   ('media/css/images', 'css/images'),
#   )
# 
# COMPILE_MEDIA_CSS = True
# COMPILE_MEDIA_CSS_METHOD = 'concat' # concat, minify
# 
# COMPILE_MEDIA_JS = True
# COMPILE_MEDIA_JS_METHOD = 'goog'
# COMPILE_MEDIA_JS_GOOG_COMPILER_PATH = \
#     "/usr/local/share/google/closure-library/closure/bin/compiler.jar"
# 
# COMPILE_MEDIA_JS_GOOG_SEARCH_PATHS = (
#   "/usr/local/share/google/closure-library",
#   "media/js",
#   )
# COMPILE_MEDIA_JS_GOOG_LEVEL = 'simple' # concat, strip, simple, advanced
# COMPILE_MEDIA_JS_GOOG_EXTERNALS = (
#   "media/js/jquery-1.3.2.min.js",
#   "media/js/jquery-ui-1.7.2.custom.min.js",
#   )

COMPILE_MEDIA_COMMON = {
  'version': 1,
  'static_dir': (
    ('media/images', 'images'),
    ('media/css/images', 'css/images'),
    )
  }

COMPILE_MEDIA_CSS_COMMON = {
  'enabled': True,
  'tool': 'csstidy',
  'csstidy': {
    'arguments': '--template=low --preserve_css=true'
    }
}

COMPILE_MEDIA_JS_COMMON = {
  'tool': 'goog_calcdeps',
  'goog_common': {
    'search_paths': (
      "/usr/local/share/google/closure-library",
      "media/js",
      ),
    'externs': (
      "media/js/jquery-1.3.2.min.js",
      "media/js/jquery-ui-1.7.2.custom.min.js",
      ),
    'use_dependency_file': False,
    },
  'goog_calcdeps': {
    'path': "/usr/local/share/google/closure-library/closure/bin/calcdeps.py",
    #'method': 'concat_refs',
    'method': 'concat',
    },
  'goog_compiler': {
    'level': 'simple',
    'path': "/usr/local/share/google/closure-library/closure/bin/compiler.jar",
    }
  }

COMPILE_MEDIA_JS = {
  'toppage.js': {
    'output_filename': 'toppage.js',
    'source_files': (
      'media/js/base.js',
      'media/js/toppage.js',
      ),
    },
  'subpages.js': {
    'goog_calcdeps': {
      'method': 'concat_refs',
      },
    'output_filename': 'subpages.js',
    'source_files': (
      'media/js/base.js',
      'media/js/subpage.js',
      ),
    },
  }

COMPILE_MEDIA_CSS = {
  'toppage.css': {
    'output_filename': 'toppage.css',
    'source_files': (
      'media/css/common.css',
      'media/css/component.css',
      'media/css/fonts.css',
      'media/css/base_layout.css',
      'media/css/toppage.css',
      ),
    },
  'subpages.css': {
    'output_filename': 'subpages.css',
    'source_files': (
      'media/css/common.css',
      'media/css/component.css',
      'media/css/fonts.css',
      'media/css/base_layout.css',
      'media/css/subpages.css',
      ),
    },
  }

