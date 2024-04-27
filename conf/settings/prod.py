from __future__ import annotations

from .base import *


print("================== PROD =================")

DEBUG = bool(os.getenv('DEBUG'))

if os.getenv('ENVIRONMENT') == 'production':
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
