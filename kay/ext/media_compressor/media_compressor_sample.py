# -*- coding: utf-8 -*-

COMPILE_MEDIA_COMMON = {
  'version': 1,
  'static_dir': (
    ('media/images', 'images'),
    ('media/css/images', 'css/images'),
  )
}

COMPILE_MEDIA_CSS_COMMON = {
  'enabled': True,
  # values for tool: 'separate' | 'concat' | 'csstidy'
  'tool': 'csstidy', 
  'csstidy': {
    #'arguments': '--template=low --preserve_css=true'
    'arguments': '--template=high'
  }
}

COMPILE_MEDIA_JS_COMMON = {
  # values for tool: None | 'concat' | 'jsminify' | 'goog_calcdeps'
  'tool': 'goog_calcdeps',  
  'goog_common': {
    # paths to closure library and others
    'search_paths': (
      "/usr/local/share/google/closure-library",
      "media/js",
    ),
    # paths to extern scripts
    'externs': (
      "media/js/jquery-1.3.2.min.js",
      "media/js/jquery-ui-1.7.2.custom.min.js",
    ),
    # whether to use deps.js at runtime
    'use_dependency_file': False,
  },
  'goog_calcdeps': {
    # path to calcdeps.py
    'path': "/usr/local/share/google/closure-library/closure/bin/calcdeps.py",
    # values for method: 'separate' | 'concat' | 'concat_refs' | 'compile'
    'method': 'concat',
  },
  'goog_compiler': {
    # values for level: 'minify' | 'simple' | 'advanced'
    'level': 'simple',
    # path to compiler.jar
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

COMPILE_MEDIA_JS_DEV = {
  'enabled': False,
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

COMPILE_MEDIA_CSS_DEV = {
  'enabled': False,
}
