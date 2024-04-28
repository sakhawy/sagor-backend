from __future__ import annotations

from .base import *


print("================== DEV ==================")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a(%m*^u0zzdiu8+^of=@ij-1e5_d&y_%@%*96yj5hmq^d=gs)r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

BASE_URL = 'http://localhost:8000'
