from django.core.management.base import BaseCommand
from email_service.consumer import Consumer
from pika.exceptions import AMQPConnectionError


class Command(BaseCommand):
    help = "Starts AMQP consumer."

    def _run_consumer(self, consumer):
        print('Consumer starts consuming...')
        try:
            consumer.connect()
        except AMQPConnectionError:
            self._run_consumer(consumer)

    def handle(self, *args, **options):
        self.stdout.write("Starting AMQP consumer...", self.style.WARNING)

        consumer = Consumer()
        self._run_consumer(consumer)
