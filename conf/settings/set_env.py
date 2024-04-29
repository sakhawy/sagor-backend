import os

_environment = os.getenv('ENVIRONMENT', None)
if _environment == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.prod")
elif _environment == "test":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.test")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.dev")
