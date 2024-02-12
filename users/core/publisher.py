import pika
from django.conf import settings
import json
from pika.exceptions import (
    ChannelWrongStateError,
    StreamLostError,
)


class Publish:
    DEFAULT_EXCHANGE = "default"
    DEFAULT_EXCHANGE_TYPE = "direct"
    DEFAULT_QUEUE = "default"
    DEFAULT_ROUTING_KEY = "default"
    DEFAULT_PROPERTIES = pika.BasicProperties(
        content_type="application/json", headers={}
    )

    def __init__(self) -> None:
        self._params = pika.URLParameters(settings.MQ_URL)
        self._conn = None
        self._channel = None

    def connect(self, exchange, exchange_type, queue, routing_key):
        if not self._conn or self._conn.is_closed:
            print('Wszedlem do connect')
            print(self._params)
            self._conn = pika.BlockingConnection(self._params)
            print('conn: ', self._conn)
            self._channel = self._conn.channel()
            self._channel.exchange_declare(
                exchange=exchange, exchange_type=exchange_type
            )
            self._channel.queue_declare(queue=queue, durable=True)
            self._channel.queue_bind(
                queue=queue, exchange=exchange, routing_key=routing_key
            )
            print('channel: ', self._channel)
        

    def _publish(self, msg, exchange, routing_key, properties):
        self._channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(msg),
            properties=properties,
        )
        print("udalo sie publishowac")

    def publish(
        self,
        msg,
        exchange=DEFAULT_EXCHANGE,
        exchange_type=DEFAULT_EXCHANGE_TYPE,
        queue=DEFAULT_QUEUE,
        routing_key=DEFAULT_ROUTING_KEY,
        properties=DEFAULT_PROPERTIES,
    ):
        print("START: publishuje msg")
        print("msg:", msg)
        try:
            self._publish(msg, exchange, routing_key, properties)
        except (AttributeError, StreamLostError, ChannelWrongStateError):
            print("except")
            self.connect(exchange, exchange_type, queue, routing_key)
            self._publish(msg, exchange, routing_key, properties)
        finally:
            self.close()

    def close(self):
        if self._conn and self._conn.is_open:
            self._conn.close()
