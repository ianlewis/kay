
from google.appengine.ext import db

class RestModel(db.Model):
  s_prop = db.StringProperty()
  i_prop = db.IntegerProperty()
  
