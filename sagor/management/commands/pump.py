import datetime
import json

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from sagor import models
from sagor.mqtt import Client


class Command(BaseCommand):
    help = "Sends signals  pumps."

    def add_arguments(self, parser):
        pass
 
    def handle(self, *args, **options):
        # the pump's domain will be identified
        # by the topic, e.g.:
        # django/main-sagor-topic/<farm-id>/<gateway-id>/<tank-id>/<pump-id>/

        # select all 'pump requests' and publish to mqtt topic
        # the save the date
        with transaction.atomic():
            # no date validation for ease of execution
            pump_requests = models.PumpedFood.objects.filter(
                status=models.PumpedFood.Status.PENDING
            ).select_for_update()

            for pump_request in pump_requests:
                sub_topic = (
                    f'{pump_request.pump.tank.gateway.farm.id}/'
                    f'{pump_request.pump.tank.gateway.id}/'
                    f'{pump_request.pump.tank.id}/'
                    f'{pump_request.pump.id}/'
                )
                topic = settings.MQTT_MAIN_TOPIC[:-1] + sub_topic
                quantity = pump_request.quantity

                # publish
                call_command(
                    'publish',
                    topic=topic,
                    broker=settings.MQTT_SERVER,
                    port=settings.MQTT_PORT,
                    message=f'''{{"quantity": {quantity} }}'''
                )

            # save
            pump_requests.update(
                status=models.PumpedFood.Status.OK,
                pumped_at=datetime.datetime.now()
            )
