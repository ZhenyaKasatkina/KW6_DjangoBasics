from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    """
    Клиент (получатель сообщений)
    """
    name = models.CharField(max_length=150, verbose_name="Имя клиента")
    email = models.EmailField(verbose_name="Адрес электронной почты")
    message = models.TextField(verbose_name="сообщение", **NULLABLE)
    owner = models.ForeignKey(
        User,
        related_name="client",
        verbose_name="владелец",
        on_delete=models.SET_NULL,
        **NULLABLE,
    )

    def __str__(self):
        # Строковое отображение объекта
        return f"Клиент: {self.name}, {self.email} ({self.message})"

    class Meta:
        verbose_name = "клиент"  # Настройка для наименования одного объекта
        verbose_name_plural = "клиенты"  # Настройка для наименования набора объектов


class Message(models.Model):
    """
    Сообщение
    """
    subject = models.CharField(max_length=150, verbose_name="Тема сообщения")
    body = models.TextField(verbose_name="сообщение")
    owner = models.ForeignKey(
        User,
        related_name="message",
        verbose_name="владелец",
        on_delete=models.SET_NULL,
        **NULLABLE,
    )

    def __str__(self):
        # Строковое отображение объекта
        return f'"{self.subject}": {self.body}'

    class Meta:
        verbose_name = "сообщение"  # Настройка для наименования одного объекта
        verbose_name_plural = "сообщения"  # Настройка для наименования набора объектов


class Newsletter(models.Model):
    """
    Рассылка сообщений
    (раз в день, раз в неделю, раз в месяц)
    """
    start_data = models.DateTimeField(verbose_name="Время начала рассылки")
    end_data = models.DateTimeField(
        verbose_name="Время завершения рассылки", **NULLABLE
    )
    ONE_TIME = "Разовая"
    ONCE_A_DAY = "Один раз в день"
    ONCE_A_WEEK = "Один раз в неделю"
    ONCE_A_MONTH = "Один раз в месяц"
    PERIODICITY = {
        ONE_TIME: "Разовая",
        ONCE_A_DAY: "Один раз в день",
        ONCE_A_WEEK: "Один раз в неделю",
        ONCE_A_MONTH: "Один раз в месяц",
    }
    periodicity = models.CharField(
        choices=PERIODICITY,
        max_length=20,
        verbose_name="Периодичность",
        default=ONCE_A_WEEK,
    )
    CREATED = "создана"
    LAUNCHED = "запущена"
    COMPLETED = "завершена"
    STATUS = {
        CREATED: "создана",
        LAUNCHED: "запущена",
        COMPLETED: "завершена",
    }
    status = models.CharField(
        choices=STATUS, max_length=15, verbose_name="Статус", default=CREATED
    )
    message = models.OneToOneField(
        Message,
        related_name="newsletter",
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
    )
    client = models.ManyToManyField(
        Client, related_name="newsletter", verbose_name="Клиент"
    )
    owner = models.ForeignKey(
        User,
        related_name="newsletter",
        verbose_name="владелец",
        on_delete=models.SET_NULL,
        **NULLABLE,
    )
    is_active = models.BooleanField(default=True, verbose_name="Статус активности")

    def __str__(self):
        # Строковое отображение объекта
        return f"дата:{self.start_data}, периодичность: {self.periodicity}, статус: {self.status}, {self.message}"

    class Meta:
        verbose_name = "рассылка"  # Настройка для наименования одного объекта
        verbose_name_plural = "рассылки"  # Настройка для наименования набора объектов
        permissions = [
            # может отключать рассылки
            ("cancel_active_status", "Can disable mailings"),
        ]


class Attempt(models.Model):
    """
    Попытка рассылки сообщений
    """
    last_data = models.DateTimeField(verbose_name="время/дата попытки")
    NOT_SENT = "не отправлено"
    SENT = "отправлено"
    STATUS = {
        NOT_SENT: "не отправлено",
        SENT: "отправлено",
    }
    status = models.CharField(
        choices=STATUS, verbose_name="Статус", default=False
    )  # успешно/не успешно
    answer = models.CharField(
        max_length=50, verbose_name="Ответ почтового сервера", **NULLABLE
    )
    # answer = models.BooleanField(default=False, verbose_name='Ответ почтового сервера')
    newsletter = models.ForeignKey(
        Newsletter,
        related_name="attempt",
        on_delete=models.CASCADE,
        verbose_name="рассылка",
    )

    def __str__(self):
        # Строковое отображение объекта
        return (
            f"Последняя попытка: {self.last_data}, "
            f"статус: {self.status}, Ответ почтового сервера: {self.answer}"
        )

    class Meta:
        verbose_name = "попытка"  # Настройка для наименования одного объекта
        verbose_name_plural = "попытки"  # Настройка для наименования набора объектов
