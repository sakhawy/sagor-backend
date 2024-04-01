import os
import django
from channels.routing import ProtocolTypeRouter
from sagor.consumers import SagorMqttConsumer
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

django.setup()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'mqtt': SagorMqttConsumer.as_asgi(),
})