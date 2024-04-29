import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from sagor.mqtt import Client


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
        message = parser.add_argument(
            '--message',
            type=str,
            default=
            '''
            {
                "farm": {
                    "id": 1,
                    "gateways": [
                        {
                            "id": 1,
                            "tanks": [
                                {
                                    "id": 1,
                                    "packages": [
                                        {
                                            "id": 1,
                                            "ph_sensor_readings": [
                                                {
                                                    "value": 0.5
                                                }
                                            ],
                                            "temprature_sensor_readings": [
                                                {
                                                    "value": 0.5
                                                }
                                            ],
                                            "camera_sensor_readings": []
                                        }
                                    ]
                                }
                            ]
                            
                        }
                    ]
                }
            }
            '''
        )

    def handle(self, *args, **options):
        # this will be dynamic, just testing shit
        topic = options['topic']
        broker = options['broker']
        port = options['port']
        message = options['message']

        client = Client(
            topic=topic,
            host=broker,
            port=port
        )

        # using load() to validate JSON
        client.publish(msg=json.dumps(json.loads(message)))
