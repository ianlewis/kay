# -*- coding: utf-8 -*-

"""
Kay framework dbutils module.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.ext import db
from google.appengine.datastore import entity_pb

import datetime
import time

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

def to_dict(model):
  output = {}

  for key in model.properties().iterkeys():
    value = getattr(model, key)

    if value is None or isinstance(value, SIMPLE_TYPES):
      output[key] = value
    elif isinstance(value, datetime.date):
      # Convert date/datetime to ms-since-epoch ("new Date()").
      ms = time.mktime(value.utctimetuple()) * 1000
      ms += getattr(value, 'microseconds', 0) / 1000
      output[key] = int(ms)
    elif isinstance(value, db.Model):
      output[key] = to_dict(value)
    else:
      output[key] = str(value)
  return output

def serialize_models(models):
 if models is None:
   return None
 elif isinstance(models, db.Model):
   # Just one instance
   return db.model_to_protobuf(models).Encode()
 else:
   # A list
   return [db.model_to_protobuf(x).Encode() for x in models]

def deserialize_models(data):
 if data is None:
   return None
 elif isinstance(data, str):
   # Just one instance
   return db.model_from_protobuf(entity_pb.EntityProto(data))
 else:
   return [db.model_from_protobuf(entity_pb.EntityProto(x)) for x in data]
