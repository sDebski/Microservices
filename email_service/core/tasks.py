from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def add(x, y):
    return x + y

@shared_task
def queue_welcome_email(username, email):
    send_mail(
        "Welcome!",
        f"Hello {username}, thanks for registration!",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

@shared_task
def queue_modify_email(username, email):
    send_mail(
        "Welcome!",
        f"Hello {username}, thanks for modification",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )