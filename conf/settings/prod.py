from __future__ import annotations

from .base import *

DEBUG = bool(os.getenv('DEBUG'))

if os.getenv('ENVIRONMENT') == 'production':
    pass
