from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .publisher import Publish
User = get_user_model()
publisher = Publish()


@receiver(post_save, sender=User)
def queue_user_save(instance, created, **kwargs):
    if not instance.email:
        return
    
    body = {"username": instance.username,
            "email": instance.email}
    
    publisher.publish(msg=body)