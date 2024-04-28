from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from sagor.mqtt import Client

# def publish(client, topic, *msgs):
#     # Generator for better control
#     for msg in msgs:
#         result = client.publish(topic, msg) 
#         status = result[0]
#         if status != 0:
#             yield msg, False
#         yield msg, True
#     yield msg, True


class Command(BaseCommand):
    help = "Publishes to all Gateways."

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
        messages = parser.add_argument(
            '--messages',
            type=str,
            nargs='?',
            default=None
        )

    def handle(self, *args, **options):
        # this will be dynamic, just testing shit
        topic = options['topic']
        broker = options['broker']
        port = options['port']
        messages = options['messages']

        client = Client(
            topic=topic,
            host=broker,
            port=port
        )

        client.publish(msg="test")
