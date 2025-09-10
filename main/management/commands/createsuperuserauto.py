# main/management/commands/createsuperuserauto.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create a superuser automatically if it doesn\'t exist'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get credentials from environment variables or use defaults
        username = os.environ.get('SUPERUSER_USERNAME', 'Wisdom')
        email = os.environ.get('SUPERUSER_EMAIL', 'wisdombesong123@gmail.com')
        password = os.environ.get('SUPERUSER_PASSWORD', 'adminpassword123')
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully!')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists.')
            )