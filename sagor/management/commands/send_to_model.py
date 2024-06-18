import datetime
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from gradio_client import Client, file

from sagor import models

class Command(BaseCommand):
    help = "Sends data to model. This command should be run twice a day at 7 & 16."

    def add_arguments(self, parser):
        pump_id = parser.add_argument(
            '--pump_id',
            type=int,
        )

    def handle(self, *args, **options):
        pump_id = options['pump_id']

        client = Client(settings.SAGOR_MODEL_CLIENT)
        # the parameters & results have confusing names i know
        results = client.predict(
            images={
                # hard-coded; fuck me
                "video": file(settings.MEDIA_ROOT / 'sagor-test.mp4')
            },
		    api_name=settings.SAGOR_MODEL_CLIENT_ENDPOINT
        )
        quantity = results.get('total_feed', 0)
        times = results.get('times', 0)
        assert times == settings.MAX_FEEDING_TIMES

        with transaction.atomic():
            today = datetime.datetime.today()
            today_at_seven = datetime.datetime(
                year=today.year,
                month=today.month,
                day=today.day,
                hour=7
            )
            today_at_sixteen = datetime.datetime(
                year=today.year,
                month=today.month,
                day=today.day,
                hour=16
            )

            valid_times = [today_at_seven, today_at_sixteen]

            for i in range(times):
                models.PumpedFood.objects.create(
                    pump_id=pump_id,
                    status=models.PumpedFood.Status.PENDING,
                    quantity=quantity,
                    should_pump_at=valid_times[i]
                )
