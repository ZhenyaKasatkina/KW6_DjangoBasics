import smtplib
from datetime import datetime

import pytz
from django.core.mail import send_mail

from config import settings
from email_newsletter.models import Newsletter, Message, Attempt


def get_next_attempt_date(
    newsletter_periodicity, current_datetime, last_attempt_last_data
):
    """Получить дату следующей попытки
    (периодичность, текущее время, дата последней попытки),
    возвращает Bool"""
    # *количество дней
    if (
        newsletter_periodicity == "Один раз в день"
        and (current_datetime - last_attempt_last_data).days >= 1
    ):
        return True
    # *количество недель
    if (
        newsletter_periodicity == "Один раз в неделю"
        and (current_datetime - last_attempt_last_data).days >= 7
    ):
        return True
    # *количество месяцев
    if (
        newsletter_periodicity == "Один раз в месяц"
        and (current_datetime - last_attempt_last_data).month >= 1
    ):
        return True


def send_message(instance_newsletter):
    """
    Отправка сообщения
    """
    messages = Message.objects.get(newsletter=instance_newsletter.pk)
    for client in instance_newsletter.client.all():
        # print(messages.body)
        send_mail(
            subject=f"{messages.subject}",
            message=f"'{messages.body}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email],
            fail_silently=False,
        )


def my_scheduled_job():
    """
    Главная функция по отправке рассылки
    """
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)  # текущее время
    print('привет!')
    # создание объекта рассылки с применением фильтра
    # время отправки которых наступило ранее текущего
    newsletters = Newsletter.objects.filter(start_data__lte=current_datetime)

    for newsletter in newsletters:
        if (
                newsletter.is_active
                and not newsletter.end_data
                and newsletter.status == "создана"
                and newsletter.start_data < current_datetime
        ):
            try:
                # - отправляем сообщение
                send_message(newsletter)
                # - изменить статус на запущена в БД/на завершена у рассылки если разовое
                if newsletter.periodicity == "Разовая":
                    newsletter.status = "завершена"
                else:
                    newsletter.status = "запущена"
                newsletter.save()
                # print(newsletter.status)

                # - создаем попытку
                new_attempt = Attempt.objects.create(
                    last_data=current_datetime,
                    status="отправлено",
                    newsletter=newsletter,
                )
                new_attempt.save()
            except smtplib.SMTPException as e:
                # При ошибке почтовика получаем ответ сервера - ошибка, которая записывается в е
                # print(e)
                new_attempt = Attempt.objects.create(
                    last_data=current_datetime,
                    status="не отправлено",
                    newsletter=newsletter,
                    answer=e,
                )
                new_attempt.save()

        if (newsletter.is_active
                and newsletter.end_data
                and newsletter.status in ("запущена", "создана",)
                and current_datetime > newsletter.end_data):
            newsletter.status = "завершена"
            newsletter.save()

        if (
                newsletter.is_active
                and newsletter.end_data
                and newsletter.status == "создана"
                and (newsletter.start_data < current_datetime < newsletter.end_data)
        ):
            try:
                # - отправляем сообщение
                send_message(newsletter)
                # - изменить статус на запущена в БД/на завершена у рассылки если разовое
                if newsletter.periodicity == "Разовая":
                    newsletter.status = "завершена"
                else:
                    newsletter.status = "запущена"
                newsletter.save()
                # print(newsletter.status)

                # - создаем попытку
                new_attempt = Attempt.objects.create(
                    last_data=current_datetime,
                    status="отправлено",
                    newsletter=newsletter,
                )
                new_attempt.save()
            except smtplib.SMTPException as e:
                # При ошибке почтовика получаем ответ сервера - ошибка, которая записывается в е
                # print(e)
                new_attempt = Attempt.objects.create(
                    last_data=current_datetime,
                    status="не отправлено",
                    newsletter=newsletter,
                    answer=e,
                )
                new_attempt.save()

        if (newsletter.is_active
                and newsletter.status == "запущена" and
                (not newsletter.end_data or (current_datetime < newsletter.end_data))):
            # print(newsletter.status)
            last_attempt = (
                Attempt.objects.filter(newsletter=newsletter.pk).order_by("last_data").last()
            )
            print(last_attempt, newsletter.message)
            if get_next_attempt_date(
                newsletter.periodicity, current_datetime, last_attempt.last_data
            ):
                try:
                    # - отправляем сообщение
                    send_message(newsletter)

                    # - создаем попытку
                    new_attempt = Attempt.objects.create(
                        last_data=current_datetime,
                        status="отправлено",
                        newsletter=newsletter,
                    )
                    new_attempt.save()
                    print(new_attempt)

                except smtplib.SMTPException as e:
                    # При ошибке почтовика получаем ответ сервера - ошибка, которая записывается в е
                    print(f"Ошибка {e}")
                    new_attempt = Attempt.objects.create(
                        last_data=current_datetime,
                        status="не отправлено",
                        newsletter=newsletter,
                        answer=e,
                    )
                    new_attempt.save()
