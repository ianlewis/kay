# -*- coding: utf-8 -*-

"""
Kay generics CRUD classes.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging
from string import Template

from google.appengine.ext import db
from werkzeug.routing import (
  Rule, RuleTemplate, EndpointPrefix, Submount,
)
from werkzeug.exceptions import (
  NotFound, Forbidden
)
from werkzeug import (
  Response, redirect
)
from werkzeug.utils import import_string
from werkzeug.routing import RequestRedirect

from kay.utils import (
  render_to_response, url_for
)
from kay.db import OwnerProperty
from kay.utils.flash import (
  set_flash, get_flash
)
from kay.exceptions import NotAuthorized
from kay.i18n import gettext as _
from kay.i18n import lazy_gettext
from kay.routing import ViewGroup

from kay.generics import (
  OP_LIST, OP_SHOW, OP_CREATE, OP_UPDATE, OP_DELETE
)

endpoints = {
  'list': "list_$model",
  'show': "show_$model",
  'create': "create_$model",
  'update': "update_$model",
  'delete': "delete_$model",
}

per_domain_endpoints = {
  'list': "a/list_$model",
  'show': "a/show_$model",
  'create': "a/create_$model",
  'update': "a/update_$model",
  'delete': "a/delete_$model",
}


class CRUDViewGroup(ViewGroup):
  entities_per_page = 20
  templates = {
    OP_LIST: '_internal/general_list.html',
    OP_SHOW: '_internal/general_show.html',
    OP_UPDATE: '_internal/general_update.html',
  }
  forms = {}
  form = None
  owner_attr = None
  rule_template = RuleTemplate([
    Rule('/$model/list', endpoint=endpoints[OP_LIST]),
    Rule('/$model/list/<cursor>', endpoint=endpoints[OP_LIST]),
    Rule('/$model/show/<key>', endpoint=endpoints[OP_SHOW]),
    Rule('/$model/create', endpoint=endpoints[OP_CREATE]),
    Rule('/$model/update/<key>', endpoint=endpoints[OP_UPDATE]),
    Rule('/$model/delete/<key>', endpoint=endpoints[OP_DELETE]),
  ])
  messages = {
    'title_update': lazy_gettext(u"Updating a %s entity"),
    'title_create': lazy_gettext(u"Creating a new %s"),
    'result_update': lazy_gettext(u"An entity is updated successfully."),
    'result_create': lazy_gettext(u"A new entity is created successfully."),
    'result_delete': lazy_gettext(u"An entity is deleted successfully."),
  }

  def __init__(self, model=None, **kwargs):
    super(CRUDViewGroup, self).__init__(**kwargs)
    self.model = model or self.model
    if isinstance(self.model, basestring):
      self.model_name = self.model.split(".")[-1]
    else:
      self.model_name = self.model.__name__
    self.model_name_lower = self.model_name.lower()

  def _import_model_if_not(self):
    if isinstance(self.model, basestring):
      self.model = import_string(self.model)

  def get_additional_context_on_create(self, request, form):
    if self.owner_attr:
      if request.user.is_anonymous():
        owner = None
      else:
        owner = request.user.key()
      return {self.owner_attr: owner}
    else:
      return {}

  def get_additional_context_on_update(self, request, form):
    return {}

  def get_query(self, request):
    created_timestamp_name = None
    for k, v in self.model.fields().iteritems():
      if isinstance(v, db.DateTimeProperty):
        if hasattr(v, 'auto_now_add') and v.auto_now_add:
          created_timestamp_name = k
    if created_timestamp_name:
      return self.model.all().order('-%s' % created_timestamp_name)
    else:
      return self.model.all()

  def get_template(self, request, name):
    return self.templates[name]

  def get_form(self, request, name):
    try:
      ret = self.forms[name]
    except KeyError:
      ret = self.form
    if isinstance(ret, basestring):
      return import_string(ret)
    else:
      return ret

  def url_for(self, *args, **kwargs):
    return url_for(*args, **kwargs)

  def get_list_url(self, cursor=None):
    return self.url_for(self.get_endpoint(OP_LIST), cursor=cursor)
  
  def get_detail_url(self, obj):
    return self.url_for(self.get_endpoint(OP_SHOW), key=obj.key())

  def get_delete_url(self, obj):
    return self.url_for(self.get_endpoint(OP_DELETE), key=obj.key())

  def get_update_url(self, obj):
    return self.url_for(self.get_endpoint(OP_UPDATE), key=obj.key())

  def get_create_url(self):
    return self.url_for(self.get_endpoint(OP_CREATE))

  def url_processor(self, request):
    return {'list_url': self.get_list_url,
            'detail_url': self.get_detail_url,
            'delete_url': self.get_delete_url,
            'update_url': self.get_update_url,
            'create_url': self.get_create_url}

  def authorize(self, request, operation, obj=None):
    """ Raise AuthorizationError when the operation is not permitted.
    """
    return True

  def check_authority(self, request, operation, obj=None):
    try:
      self.authorize(request, operation, obj)
    except NotAuthorized, e:
      from kay.conf import settings
      if 'kay.auth.middleware.AuthenticationMiddleware' in \
            settings.MIDDLEWARE_CLASSES and \
            request.user.is_anonymous():
        from kay.utils import create_login_url
        raise RequestRedirect(create_login_url(request.url))
      else:
        raise Forbidden("Access not allowed.")

  def list(self, request, cursor=None):
    # TODO: bi-directional pagination instead of one way ticket forward
    self._import_model_if_not()
    self.check_authority(request, OP_LIST)
    q = self.get_query(request)
    if cursor:
      q.with_cursor(cursor)
    entities = q.fetch(self.entities_per_page)
    if entities:
      next_cursor = q.cursor()

      q2 = self.get_query(request)
      q2.with_cursor(next_cursor)
      if q2.get() is None:
        next_cursor = None
    else:
      next_cursor = None
    return render_to_response(self.get_template(request, OP_LIST),
                              {'model': self.model_name,
                               'entities': entities,
                               'cursor': next_cursor,
                               'message': get_flash(),
                              },
                              processors=(self.url_processor,))

  def show(self, request, key):
    from google.appengine.api.datastore_errors import BadKeyError
    self._import_model_if_not()
    try:
      entity = db.get(key)
    except BadKeyError, e:
      logging.warn("Failed to get an entity: %s" % e)
      entity = None
    if entity is None:
      raise NotFound("Specified %s not found." % self.model_name)
    self.check_authority(request, OP_SHOW, entity)
    sorted_props = [
      (prop_name, prop.verbose_name if prop.verbose_name else prop_name,
       entity.__getattribute__(prop_name))
      for prop_name, prop in
      sorted(entity.fields().items(), key=lambda x: x[1].creation_counter)
    ]
    # TODO: deal with dynamic_properties
    
    return render_to_response(self.get_template(request, OP_SHOW),
                              {'entity': entity,
                               'model': self.model_name,
                               'sorted_props': sorted_props},
                              processors=(self.url_processor,))

  def create_or_update(self, request, key=None):
    from google.appengine.api.datastore_errors import BadKeyError
    self._import_model_if_not()
    if key:
      try:
        entity = db.get(key)
      except BadKeyError:
        entity = None
      if entity is None:
        raise NotFound("Specified %s not found." % self.model_name)
      form_class = self.get_form(request, OP_UPDATE)
      form = form_class(instance=entity)
      title = self.messages['title_update'] % self.model_name
      self.check_authority(request, OP_UPDATE, entity)
    else:
      form_class = self.get_form(request, OP_CREATE)
      form = form_class()
      title = self.messages['title_create'] % self.model_name
      self.check_authority(request, OP_CREATE)
    if request.method == 'POST':
      if form.validate(request.form, request.files):
        if key:
          additional_context = self.get_additional_context_on_update(request,
                                                                     form)
          message = self.messages['result_update']
        else:
          additional_context = self.get_additional_context_on_create(request,
                                                                     form)
          message = self.messages['result_create']
        new_entity = form.save(**additional_context)
        set_flash(message)
        return redirect(self.get_list_url())
    return render_to_response(self.get_template(request, OP_UPDATE),
                              {'form': form.as_widget(),
                               'title': title},
                              processors=(self.url_processor,))

  def create(self, *args, **kwargs):
    return self.create_or_update(*args, **kwargs)

  def update(self, *args, **kwargs):
    return self.create_or_update(*args, **kwargs)

  def delete(self, request, key):
    from google.appengine.api.datastore_errors import BadKeyError
    self._import_model_if_not()
    try:
      entity = db.get(key)
    except BadKeyError:
      # just ignore it
      entity = None
    if entity is None:
      raise NotFound("Specified %s not found." % self.model_name)
    self.check_authority(request, OP_DELETE, entity)
    entity.delete()
    set_flash(self.messages['result_delete'])
    # TODO: back to original page
    return redirect(self.get_list_url())
    
  def _get_rules(self):
    return [self.rule_template(model=self.model_name_lower)]

  def _get_views(self, prefix=None):
    self.prefix = prefix
    ret = {}
    for key, val in self.endpoints.iteritems():
      s = Template(val)
      endpoint = s.substitute(model=self.model_name_lower)
      if prefix:
        endpoint = prefix+endpoint
      ret[endpoint] = self.get_method(key)
    return ret

  def get_method(self, key):
    return getattr(self, key)

  def get_endpoint(self, key):
    endpoint = Template(self.endpoints[key]).\
        substitute(model=self.model_name_lower)
    if self.prefix:
      endpoint = self.prefix+endpoint
    return endpoint

  @property
  def endpoints(self):
    return endpoints

class PerDomainCRUDViewGroup(CRUDViewGroup):
  rule_template = RuleTemplate([
    Rule('/a/<domain_name>/$model/list',
         endpoint=per_domain_endpoints[OP_LIST]),
    Rule('/a/<domain_name>$model/list/<cursor>',
         endpoint=per_domain_endpoints[OP_LIST]),
    Rule('/a/<domain_name>/$model/show/<key>',
         endpoint=per_domain_endpoints[OP_SHOW]),
    Rule('/a/<domain_name>/$model/create',
         endpoint=per_domain_endpoints[OP_CREATE]),
    Rule('/a/<domain_name>/$model/update/<key>',
         endpoint=per_domain_endpoints[OP_UPDATE]),
    Rule('/a/<domain_name>/$model/delete/<key>',
         endpoint=per_domain_endpoints[OP_DELETE]),
  ])

  def extract_domain(self, func):
    def inner(*args, **kwargs):
      self.domain = kwargs.pop('domain_name')
      return func(*args, **kwargs)
    return inner

  def get_method(self, key):
    return self.extract_domain(getattr(self, key))
  
  def url_for(self, *args, **kwargs):
    kwargs['domain_name'] = self.domain
    return url_for(*args, **kwargs)

  @property
  def endpoints(self):
    return per_domain_endpoints
