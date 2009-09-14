# -*- coding: utf-8 -*-

"""
Kay framework dbutils module.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.ext import db
from google.appengine.datastore import entity_pb

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
