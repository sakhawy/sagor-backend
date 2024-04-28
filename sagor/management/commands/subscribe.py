from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from sagor.mqtt import Client

class Command(BaseCommand):
    help = "Subscribes to all Gateways."

    def add_arguments(self, parser):
        topic = parser.add_argument(
            "--topic", 
            type=str,
            default=settings.MQTT_MAIN_TOPIC
        )
        broker = parser.add_argument(
            "--broker", 
            type=str,
            nargs='?',
            default=settings.MQTT_SERVER
        )
        port = parser.add_argument(
            "--port", 
            type=int,
            nargs='?',
            default=settings.MQTT_PORT
        )

    def handle(self, *args, **options):
        topic = options['topic']
        broker = options['broker']
        port = options['port']

        client = Client(
            topic=topic,
            host=broker,
            port=port
        )

        client.subscribe()
