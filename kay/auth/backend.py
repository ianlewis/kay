# -*- coding: utf-8 -*-

"""
Kay authentication backends.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging

from kay.auth.backends.googleaccount import GoogleBackend
from kay.auth.backends.datastore import (
  DatastoreBackend, DatastoreBackendWithOwnedDomainHack
)

logging.warn("Deprecation warning. Importing auth backend from 'kay.auth.backend' module is deprecated. Please import these backends from 'kay.auth.backends.googleaccount' or 'kay.auth.backends.datastore' module instead.")
