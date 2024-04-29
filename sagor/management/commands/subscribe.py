import uuid

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from sagor.mqtt import Client
from sagor import models as sagor_models


def save_to_database(payload):
    # NOTE: This will be super dirty
    # got no time to fix this dumpster fire

    # NOTE: FOR THE LOVE OF GOD USE A FUCKING SERIALIZER
    # TO DO THIS SHIT WTF AM I DOING TO MYSELF
    farm = payload.pop('farm', None)
    if farm:
        farm_model, created = sagor_models.Farm.objects.get_or_create(
            id=farm['id'],
            defaults=dict(name=uuid.uuid4())
        )
        gateways = farm.pop('gateways', None)
        if isinstance(gateways, list):
            for gateway in gateways:
                gateway_model, created = sagor_models.Gateway.objects.get_or_create(
                    id=gateway['id'],
                    farm_id=farm_model.id,
                    defaults=dict(
                        status=sagor_models.Gateway.Status.OK
                    )
                )
                tanks = gateway.pop('tanks', None)
                if isinstance(tanks, list):
                    for tank in tanks:
                        tank_model, created = sagor_models.Tank.objects.get_or_create(
                            id=tank['id'],
                            gateway_id=gateway_model.id
                        )
                        packages = tank.pop('packages', None)
                        if isinstance(packages, list):
                            for package in packages:
                                package_model, created = sagor_models.Package.objects.get_or_create(
                                    id=package['id'],
                                    tank_id=tank_model.id,
                                    defaults=dict(
                                        status=sagor_models.Gateway.Status.OK
                                    )
                                )
                                ph_sensor_readings = package.pop('ph_sensor_readings', None)
                                if isinstance(ph_sensor_readings, list):
                                    for reading in ph_sensor_readings:
                                        sagor_models.PHSensorReading.objects.create(
                                            value=reading['value'],
                                            reading_status=sagor_models.PHSensorReading.ReadingStatus.SANE,
                                            read_every='1000',
                                            package_id=package_model.id
                                        )
                                else:
                                    raise Exception()

                                temprature_sensor_readings = package.pop('temprature_sensor_readings', None)
                                if isinstance(temprature_sensor_readings, list):
                                    for reading in temprature_sensor_readings:
                                        sagor_models.PHSensorReading.objects.create(
                                            value=reading['value'],
                                            reading_status=sagor_models.TempratureSensorReading.ReadingStatus.SANE,
                                            read_every='1000',
                                            package_id=package_model.id
                                        )
                                else:
                                    raise Exception()
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
