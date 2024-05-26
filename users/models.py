from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """
    Пользователь
    """
    username = None
    email = models.EmailField(unique=True, verbose_name='Адрес электронной почты')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name='аватар', **NULLABLE)

    token = models.CharField(max_length=100, verbose_name="token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"  # Настройка для наименования одного объекта
        verbose_name_plural = "пользователи"    # Настройка для наименования набора объектов
        permissions = [
            # может блокировать пользователей сервиса
            ("cancel_active_status", "Can block service users"),
            # может просматривать список пользователей сервиса
            ("can_view_list_users", "Can view the list of service users")
            ]
