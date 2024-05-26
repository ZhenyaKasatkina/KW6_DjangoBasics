from django.core.management import BaseCommand

from config.settings import EMAIL_HOST_USER, SUPERUSER_PASSWORD
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Создание суперпользователя
        """
        user = User.objects.create(
            email=EMAIL_HOST_USER
        )
        user.set_password(SUPERUSER_PASSWORD)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
