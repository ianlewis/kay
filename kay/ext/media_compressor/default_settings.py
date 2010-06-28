COMPILE_MEDIA = {
  'version': 1,
  'enabled': True,
  'output_base_dir': '_generated_media',
}

COMPILE_MEDIA_CSS = {
  'subdir': 'css',
  'tool': 'concat', # 'separate' | 'concat' | 'csstidy'
  'csstidy': {
    'path': 'csstidy',
    'arguments': '--template=high',
  },
  'source_files': (),
  'source_urls': (),
  'output_filename': None,
}

COMPILE_MEDIA_CSS_DEV = {
  'enabled': False,
}

COMPILE_MEDIA_JS = {
  'subdir': 'js',
  # 'concat' | 'jsminify' | 'goog_calcdeps' | 'goog_compiler'
  'tool': 'jsminify',
  'goog_common': {
    'externs': (),      # paths to extern scripts
    # paths to closure library and others
    'search_paths': ('/usr/local/closure-library',), 
    'use_dependency_file': False, # whether to use deps.js at runtime
  },
  'goog_calcdeps': {
    # path to calcdeps.py
    'path': '/usr/local/closure-library/closure/bin/calcdeps.py',
    'method': 'concat_refs', #'separate' | 'concat' | 'concat_refs' | 'compile'
  },
  'goog_compiler': {
    'level': 'simple', # 'minify' | 'simple' | 'advanced'
    'path': '/usr/local/closure-compiler/compiler.jar', # path to compiler.jar
  },
  'source_files': (),
  'source_urls': (),
  'output_filename': None,
}

COMPILE_MEDIA_JS_DEV = {
  'enabled': False,
}
