
from kay.utils import local
from jinja2 import Template

wrapped = False
render_orig = Template.render

def wrapper(self, *args, **kwargs):
  import logging
  if not hasattr(local, 'used_templates'):
    local.used_templates = []
  if not hasattr(local, 'used_contexts'):
    local.used_contexts = []
  vars = dict(*args, **kwargs)
  local.used_templates.append(self.name)
  local.used_contexts.append(vars)
  return render_orig(self, *args, **kwargs)

def init_recording():
  local.used_templates = []
  local.used_contexts = []
  global wrapped
  if not wrapped:
    Template.render = wrapper
    wrapped = True

def get_templates():
  if not hasattr(local, 'used_templates'):
    local.used_templates = []
  return local.used_templates

def get_last_template():
  templates = get_templates()
  if templates:
    return templates[-1]

def get_contexts():
  if not hasattr(local, 'used_contexts'):
    local.used_contexts = []
  return local.used_contexts

def get_last_context():
  contexts = get_contexts()
  if contexts:
    return contexts[-1]
