from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Creates an admin user"

    def handle(self, *args, **kwargs):
        if User.objects.filter(username="admin").exists():
            self.stdout.write("Admin user already exists", self.style.WARNING)
            return
        
        User.objects.create_superuser(username='admin', password="admin")
        self.stdout.write("Admin user has been created", self.style.SUCCESS)