from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Subscribes to all Gateways."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
