import uuid

from django.conf import settings
from paho.mqtt import client as mqtt_client


class Client:
    def __new__(self):
        # client id has to be unique
        self.client_id = f'{settings.MQTT_CLIENT_ID_PREFIX}_{uuid.uuid4()}'
        self.topic = settings.MQTT_MAIN_TOPIC
        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
        self.client.connect(
            host=settings.MQTT_SERVER,
            port=settings.MQTT_PORT,
            keepalive=settings.MQTT_KEEPALIVE
        )
        self.client.subscribe(self.topic)
        return self.client

    def on_connect(self, userdata, flags, rc):
        if rc != 0:
            raise Exception('Couldn\'t connect')

    def on_message(self, userdata, msg):
        pass
