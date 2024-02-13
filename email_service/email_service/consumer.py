import json
import pika
from django.conf import settings
from core import tasks


class Consumer:
    QUEUES_CALLBACKS = {
        "email_service_queue": "get_email_data",
    }

    def __init__(self):
        self._params = pika.URLParameters(settings.MQ_URL)
        self._conn = None
        self._channel = None

    def connect(self):
        if not self._conn or self._conn.is_closed:
            print(f"Connecting to {settings.MQ_URL}")
            self._conn = pika.BlockingConnection(self._params)
            self._channel = self._conn.channel()
    
    def get_email_data(self, channel, method, properties, body):

        decoded = body.decode()
        user, email = json.loads(decoded).values()

        print(user, email)

        tasks.queue_send_email.delay(user, email)

    
    def _bind_queues_to_callback(self):
        for queue, callback in self.QUEUES_CALLBACKS.items():
            self._channel.queue_declare(queue=queue, durable=True)
            self._channel.basic_consume(queue=queue, on_message_callback=getattr(self, callback), auto_ack=True)

    def consume(self):
        self._bind_queues_to_callback()
        self._channel.start_consuming()

    def close(self):
        if self._conn and self._conn.is_open():
            self._conn.close()