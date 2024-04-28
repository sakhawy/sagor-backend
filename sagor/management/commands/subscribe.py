from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from sagor.mqtt import Client

class Command(BaseCommand):
    help = "Subscribes to all Gateways."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        client = Client()
        client.loop_forever()
