import json
import uuid

from django.conf import settings
from paho.mqtt import client as mqtt_client


class Client:
    def __init__(
            self,
            topic=settings.MQTT_MAIN_TOPIC,
            host=settings.MQTT_SERVER,
            port=settings.MQTT_PORT,
            on_message_callback=lambda payload: ...,
            keepalive=settings.MQTT_KEEPALIVE,
            user=settings.MQTT_USER,
            password=settings.MQTT_PASSWORD,
        ):
        # client id has to be unique
        self._client_id=f'{settings.MQTT_CLIENT_ID_PREFIX}_{uuid.uuid4()}'
        self.topic = topic
        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, self._client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(user, password)
        self.client.connect(
            host=host,
            port=port,
            keepalive=keepalive
        )
        self.on_message_callback = on_message_callback

    def on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            raise Exception('Couldn\'t connect')

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            print(payload)
        except Exception as e:
            raise Exception(e)
        
        self.on_message_callback(payload)

    def subscribe(self):
        try:
            self.client.subscribe(self.topic)
            self.client.loop_forever()
        except Exception as e:
            raise Exception(e)

        return True

    def publish(self, msg, topic=settings.MQTT_MAIN_TOPIC[:-1]):
        # consider feeding a generator to
        # the method and yield the result
        try:
            self.client.loop_start()
            self.client.publish(topic, msg)
            self.client.loop_stop()
        except Exception as e:
            raise Exception(e)

        return True
