from django.core.management.base import BaseCommand, CommandError
from paho.mqtt import client as mqtt_client

def connect_client(topic, broker, port):
    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION1,
        topic
    )

    # Do some error checking here
    client.on_connect = None
    client.connect(broker, port)
    return client


def publish(client, topic, *msgs):
    # Generator for better control
    for msg in msgs:
        result = client.publish(topic, msg) 
        status = result[0]
        if status != 0:
            yield msg, False
        yield msg, True
    yield msg, True


class Command(BaseCommand):
    help = "Publishes to all Gateways."

    def add_arguments(self, parser):
        topic = parser.add_argument(
            "topic", 
            type=str,
            default=None
        )
        broker = parser.add_argument(
            "--broker", 
            type=str,
            nargs='?',
            default='broker.emqx.io'
        )
        port = parser.add_argument(
            "--port", 
            type=int,
            nargs='?',
            default=1883
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

        client = connect_client(
            topic,
            broker,
            port
        )

        for sent in publish(
            client,
            topic,
            *messages 
        ):
            print(sent)
