from os import getenv

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email=getenv('ADMIN_EMAIL'),
            first_name='Admin',
            last_name='Test',
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        user.set_password(getenv('ADMIN_PASSWORD'))
        user.save()
