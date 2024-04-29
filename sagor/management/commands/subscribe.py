from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from rest_framework.serializers import Serializer

from sagor.mqtt import Client
from sagor import models as sagor_models
from sagor import serializers as sagor_serializers


def save_to_database(payload):
    iot_data_serializer = sagor_serializers.IoTDataSerializer(data=payload)
    iot_data_serializer.is_valid(raise_exception=True)
    iot_data_serializer.save()


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
            port=port,
            on_message_callback=save_to_database
        )

        client.subscribe()
