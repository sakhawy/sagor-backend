from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from sagor.mqtt import Client


def save_to_database(payload):
    # NOTE: This will be super dirty
    # got no time to fix this dumpster fire
    farm = payload.pop('farm', None)
    if farm:
        gateways = farm.pop('gateways', None)
        if isinstance(gateways, list):
            for gateway in gateways:
                packages = gateway.pop('packages', None)
                if isinstance(packages, list):
                    for package in packages:
                        sensors = package.pop('sensors', None)
                        if isinstance(sensors, list):
                            for sensor in sensors:
                                # save them here!
                                pass
                        else:
                            raise Exception()
                else:
                    raise Exception()
        else:
            raise Exception()
    else:
        raise Exception()
    

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
