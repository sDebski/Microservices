from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def queue_send_email(username, email):
    send_mail(
        "Welcome!",
        f"Hello {username}, here is a message for you!",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
