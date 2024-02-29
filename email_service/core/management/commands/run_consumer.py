from django.core.management.base import BaseCommand
from email_service.consumer import Consumer
from pika.exceptions import AMQPConnectionError
import time

class Command(BaseCommand):
    help = "Starts AMQP consumer."

    def _run_consumer(self, consumer):
        print('Consumer starts consuming...')
        try:
            consumer.connect()
            
        except AMQPConnectionError:
            time.sleep(1)
            self._run_consumer(consumer)

        consumer.consume()

    def handle(self, *args, **options):
        self.stdout.write("Starting AMQP consumer...", self.style.WARNING)

        consumer = Consumer()
        self._run_consumer(consumer)
