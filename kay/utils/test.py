
from kay.utils import local
from jinja2 import Template

wrapped = False
render_orig = Template.render

def wrapper(self, *args, **kwargs):
  vars = dict(*args, **kwargs)
  local._used_templates.append(self.name)
  local._used_contexts.append(vars)
  return render_orig(self, *args, **kwargs)

def init_recordings():
  local._used_templates = []
  local._used_contexts = []

def disable_recording():
  init_recordings()
  global wrapped
  if wrapped:
    Template.render = render_orig
    wrapped = False

def init_recording():
  init_recordings()
  global wrapped
  if not wrapped:
    Template.render = wrapper
    wrapped = True

def get_templates():
  if not hasattr(local, '_used_templates'):
    local._used_templates = []
  return local._used_templates

def get_last_template():
  templates = get_templates()
  if templates:
    return templates[-1]

def get_contexts():
  if not hasattr(local, '_used_contexts'):
    local._used_contexts = []
  return local._used_contexts

def get_last_context():
  contexts = get_contexts()
  if contexts:
    return contexts[-1]