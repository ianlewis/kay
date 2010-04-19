
from google.appengine.ext import db

from kay.utils import local

class OwnerProperty(db.ReferenceProperty):
  def default_value(self):
    if hasattr(local, 'request') and hasattr(local.request, 'user'):
      if local.request.user.is_anonymous():
        return None
      else:
        return local.request.user.key()
    return None
        
