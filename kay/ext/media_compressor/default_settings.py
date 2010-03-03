COMPILE_MEDIA = {
  'version': None,
  'enabled': True,
  'output_base_dir': '_generated_media',
}

COMPILE_MEDIA_CSS = {
  'subdir': 'css',
  'tool': 'csstidy', # 'separate' | 'concat' | 'csstidy'
  'csstidy': {
    'path': 'csstidy',
    'arguments': '--template=high',
  },
  'source_files': (),
  'output_filename': None,
}

COMPILE_MEDIA_JS = {
  'subdir': 'js',
  # None | 'jsminify' | 'goog_calcdeps' | 'goog_compiler'
  'tool': 'goog_calcdeps',
  'goog_common': {
    'externs': (),      # paths to extern scripts
    'search_paths': (), # paths to closure library and others
    'use_dependency_file': False, # whether to use deps.js at runtime
  },
  'goog_calcdeps': {
    'path': None,       # path to calcdeps.py
    'method': 'concat', # 'separate' | 'concat' | 'concat_refs' | 'compile'
  },
  'goog_compiler': {
    'level': 'simple',  # 'minify' | 'simple' | 'advanced'
    'path': None,       # path to compiler.jar
  },
  'source_files': (),
  'output_filename': None,
}

