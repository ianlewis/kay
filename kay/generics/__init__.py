# -*- coding: utf-8 -*-

"""
Kay generics.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from string import Template

from werkzeug.routing import (
  Rule, RuleTemplate,
)
from werkzeug.exceptions import NotFound
from werkzeug import (
  Response, redirect
)

from kay.utils import (
  render_to_response, url_for
)
from kay.i18n import lazy_gettext as _

endpoints = {
  'list': "list_$model",
  'show': "show_$model",
  'create': "create_$model",
  'update': "update_$model",
  'delete': "delete_$model",
}

# Move this rules to class attr for customization
generic_rules = RuleTemplate([
  Rule('/$model/list', endpoint=endpoints['list']),
  Rule('/$model/list/<cursor>', endpoint=endpoints['list']),
  Rule('/$model/show/<key>', endpoint=endpoints['show']),
  Rule('/$model/create', endpoint=endpoints['create']),
  Rule('/$model/update/<key>', endpoint=endpoints['update']),
  Rule('/$model/delete/<key>', endpoint=endpoints['delete']),
])


class CRUDViewGroup(object):
  entities_per_page = 20
  templates = {
    'list': '_internal/general_list.html',
    'show': '_internal/general_show.html',
    'update': '_internal/general_update.html',
  }
  forms = {}
  form = None

  def __init__(self, model=None):
    self.model = model or self.model
    self.model_name = self.model.__name__
    self.model_name_lower = self.model_name.lower()

  def get_additional_context_on_create(self, request, form):
    return {}

  def get_additional_context_on_update(self, request, form):
    return {}

  def get_query(self):
    return self.model.all()

  def get_template(self, name):
    return self.templates[name]

  def get_form(self, name):
    try:
      return self.forms[name]
    except KeyError:
      return self.form

  def get_list_url(self, cursor=None):
    return url_for(self.get_endpoint('list'), cursor=cursor)

  def get_detail_url(self, obj):
    return url_for(self.get_endpoint('show'), key=obj.key())

  def get_delete_url(self, obj):
    return url_for(self.get_endpoint('delete'), key=obj.key())

  def get_update_url(self, obj):
    return url_for(self.get_endpoint('update'), key=obj.key())

  def get_create_url(self):
    return url_for(self.get_endpoint('create'))

  def url_processor(self, request):
    return {'list_url': self.get_list_url,
            'detail_url': self.get_detail_url,
            'delete_url': self.get_delete_url,
            'update_url': self.get_update_url,
            'create_url': self.get_create_url}

  def list(self, request, cursor=None):
    # TODO: bi-directional pagination instead of one way ticket forward
    q = self.get_query()
    if cursor:
      q = q.with_cursor(cursor)
    entities = q.fetch(self.entities_per_page)
    next_cursor = q.cursor()
    q = q.with_cursor(next_cursor)
    if q.get() is None:
      next_cursor = None
    return render_to_response(self.get_template('list'),
                              {'model': self.model_name,
                               'entities': entities,
                               'cursor': next_cursor,
                              },
                              processors=(self.url_processor,))

  def show(self, request, key):
    from google.appengine.api.datastore_errors import BadKeyError
    try:
      entity = self.model.get(key)
    except BadKeyError:
      # just ignore it
      entity = None
    if entity is None:
      raise NotFound("Specified %s not found." % self.model_name)
    return render_to_response(self.get_template('show'),
                              {'entity': entity,
                               'model': self.model_name},
                              processors=(self.url_processor,))

  def create_or_update(self, request, key=None):
    from google.appengine.api.datastore_errors import BadKeyError
    if key:
      try:
        entity = self.model.get(key)
      except BadKeyError:
        entity = None
      if entity is None:
        raise NotFound("Specified %s not found." % self.model_name)
      form_class = self.get_form('update')
      form = form_class(instance=entity)
      title = _("Updating a %s entity") % self.model_name
    else:
      form_class = self.get_form('create')
      form = form_class()
      title = _("Creating a new %s") % self.model_name
    if request.method == 'POST':
      if form.validate(request.form, request.files):
        if key:
          additional_context = self.get_additional_context_on_update(request,
                                                                     form)
        else:
          additional_context = self.get_additional_context_on_create(request,
                                                                     form)
        new_entity = form.save(**additional_context)
        # TODO: flash message
        return redirect(self.get_list_url())
    return render_to_response(self.get_template('update'),
                              {'form': form.as_widget(),
                               'title': title,
                               },
                              processors=(self.url_processor,))
    
  create = create_or_update
  update = create_or_update

  def delete(self, request, key):
    from google.appengine.api.datastore_errors import BadKeyError
    try:
      entity = self.model.get(key)
    except BadKeyError:
      # just ignore it
      entity = None
    if entity is None:
      raise NotFound("Specified %s not found." % self.model_name)
    entity.delete()
    # TODO: flash message
    # TODO: back to original page
    return redirect(self.get_list_url())
    

  def get_rules(self):
    return generic_rules(model=self.model_name_lower)

  def get_views(self, prefix=None):
    self.prefix = prefix
    ret = {}
    for key, val in endpoints.iteritems():
      s = Template(val)
      endpoint = s.substitute(model=self.model_name_lower)
      if prefix:
        endpoint = prefix+endpoint
      ret[endpoint] = getattr(self, key)
    return ret

  def get_endpoint(self, key):
    endpoint = Template(endpoints[key]).substitute(model=self.model_name_lower)
    if self.prefix:
      endpoint = self.prefix+endpoint
    return endpoint
