import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from email_newsletter.forms import (
    NewsletterForm,
    NewsletterModeratorForm,
    NewsletterModeratorOwnerForm,
    ClientForm,
    MessageForm,
)
from email_newsletter.models import Newsletter, Client, Message, Attempt
from email_newsletter.services import get_blog_from_cache


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    extra_context = {
        "title": "Здесь находится список Ваших рассылок",
        "text": "Рассылки используются не только для рекламы, "
        "но и чтобы помочь пользователю разобраться в продукте "
        "(например, рассказать о возможностях сервиса); "
        "сообщить важную информацию о заказе и сроках его доставки; "
        "наладить обратную связь с клиентом, например собрать отзывы о покупке.",
        "create_object": "Создать новую рассылку",
    }

    def get_context_data(self, **kwargs):
        """
        Права доступа на просмотр всех рассылок и возможность отключения рассылок.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user.has_perm("email_newsletter.view_newsletter") and user.has_perm(
            "email_newsletter.cancel_active_status"
        ):
            return context_data
        else:
            object_list = list(
                filter(
                    lambda x: (x.owner == user),
                    Newsletter.objects.filter(is_active=True),
                )
            )
            # print(object_list)
            context_data["object_list"] = object_list
            return context_data


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("email_newsletter:newsletter")
    extra_context = {
        "title": "Здесь создаем новую рассылку",
        "text": "Рассылки используются не только для рекламы, "
        "но и чтобы помочь пользователю разобраться в продукте "
        "(например, рассказать о возможностях сервиса); "
        "сообщить важную информацию о заказе и сроках его доставки; "
        "наладить обратную связь с клиентом, например собрать отзывы о покупке.",
    }

    def get_form_kwargs(self):
        """
        Передача текущего пользователя в форму
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        """
        Автоматическое добавление текущего пользователям как создателя рассылки
        """
        if form.is_valid():
            self.object = form.save()
            user = self.request.user
            self.object.owner = user
            self.object.save()
            # print(self.object)
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    success_url = reverse_lazy("email_newsletter:newsletter")
    extra_context = {
        "title": "Здесь можно изменить данные рассылки",
        "text": "Рассылки используются не только для рекламы, "
        "но и чтобы помочь пользователю разобраться в продукте "
        "(например, рассказать о возможностях сервиса); "
        "сообщить важную информацию о заказе и сроках его доставки; "
        "наладить обратную связь с клиентом, например собрать отзывы о покупке.",
    }

    def get_form_class(self):
        """
        Права доступа владельца, менеджера.
        """
        user = self.request.user
        if (
            user == self.object.owner
            and self.object.is_active
            and user.has_perm("email_newsletter.cancel_active_status")
        ) or user.is_superuser:
            return NewsletterModeratorOwnerForm
        if user.has_perm("email_newsletter.cancel_active_status"):
            return NewsletterModeratorForm
        if user == self.object.owner and self.object.is_active:
            return NewsletterForm
        raise PermissionDenied

    def get_form_kwargs(self):
        """
        Передача текущего пользователя в форму
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy("email_newsletter:newsletter")
    extra_context = {
        "title": "Здесь можно удалить рассылку",
        "text": "Рассылки используются не только для рекламы, "
        "но и чтобы помочь пользователю разобраться в продукте "
        "(например, рассказать о возможностях сервиса); "
        "сообщить важную информацию о заказе и сроках его доставки; "
        "наладить обратную связь с клиентом, например собрать отзывы о покупке.",
    }

    def get_context_data(self, **kwargs):
        """
        Права доступа владельца.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner:
            return context_data
        raise PermissionDenied


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter
    permission_required = "email_newsletter.view_newsletter"

    extra_context = {
        "title": "Вот все данные по рассылке",
        "text": "Рассылки используются не только для рекламы, "
        "но и чтобы помочь пользователю разобраться в продукте "
        "(например, рассказать о возможностях сервиса); "
        "сообщить важную информацию о заказе и сроках его доставки; "
        "наладить обратную связь с клиентом, например собрать отзывы о покупке.",
        "create_object": "Создать новую рассылку",
    }

    def get_context_data(self, **kwargs):
        """
        Права доступа владельца, менеджера.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner or user.has_perm(
            "email_newsletter.view_newsletter"
        ):
            return context_data
        raise PermissionDenied


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        "title": "Здесь находится список Ваших клиентов",
        "text": "Лояльность клиентов – это нематериальный, но чрезвычайно "
        "ценный актив компании. Способность объективно оценивать и "
        "влиять на лояльность потребителей – важный инструмент "
        "для достижения бизнес-целей, сохранения и расширения клиентской базы.",
        "create_object": "Создать нового клиента",
    }

    def get_context_data(self, **kwargs):
        """
        Права доступа на просмотр всех клиентов.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser:
            return context_data
        else:
            object_list = list(
                filter(lambda x: (x.owner == user), Client.objects.all())
            )
            context_data["object_list"] = object_list
            return context_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("email_newsletter:client")
    extra_context = {
        "title": "Здесь создаем нового клиента",
        "text": "Лояльность клиентов – это нематериальный, но чрезвычайно "
        "ценный актив компании. Способность объективно оценивать и "
        "влиять на лояльность потребителей – важный инструмент "
        "для достижения бизнес-целей, сохранения и расширения клиентской базы.",
    }

    def form_valid(self, form):
        """
        Автоматическое добавление текущего пользователям как создателя клиента
        """
        if form.is_valid():
            self.object = form.save()
            user = self.request.user
            self.object.owner = user
            self.object.save()
            # print(self.object)
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("email_newsletter:client")
    extra_context = {
        "title": "Здесь можно изменить данные клиента",
        "text": "Лояльность клиентов – это нематериальный, но чрезвычайно "
        "ценный актив компании. Способность объективно оценивать и "
        "влиять на лояльность потребителей – важный инструмент "
        "для достижения бизнес-целей, сохранения и расширения клиентской базы.",
    }

    def get_context_data(self, **kwargs):
        """
        Права доступа владельца, менеджера.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner:
            return context_data
        raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("email_newsletter:client")
    extra_context = {
        "title": "Здесь можно удалить Клиента",
        "text": "Если больше не планируете работать с этим клиентом - "
        "то его можно удалить из Вашего Списка клиентов. ."
        "Но помните: Лояльность клиентов – это нематериальный, но чрезвычайно "
        "ценный актив компании.",
    }

    def get_context_data(self, **kwargs):
        """
        Права доступа владельца.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner:
            return context_data
        raise PermissionDenied


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    extra_context = {
        "title": "Вот полные данные клиента",
        "text": "Лояльность клиентов – это нематериальный, но чрезвычайно "
        "ценный актив компании. Способность объективно оценивать и "
        "влиять на лояльность потребителей – важный инструмент "
        "для достижения бизнес-целей, сохранения и расширения клиентской базы.",
        "create_object": "Создать нового клиента",
    }


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {
        "title": "Здесь находятся Ваши сообщения для клиентов",
        "text": "Интересный заголовок, краткое и ясное содержание, "
        "призыв к действию. Вы должны максимально упростить жизнь клиенту "
        "и избегать длинных непонятных текстов. Не скатывайтесь в повествование, "
        "помните, что у каждого сообщения должна быть цель.",
        "create_object": "Создать новое сообщение",
    }

    def get_context_data(self, **kwargs):
        """
        Права доступа на просмотр всех сообщений.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser:
            return context_data
        else:
            object_list = list(
                filter(lambda x: (x.owner == user), Message.objects.all())
            )
            context_data["object_list"] = object_list
            return context_data


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("email_newsletter:message")
    extra_context = {
        "title": "Здесь создаем сообщения для клиентов",
        "text": "Интересный заголовок, краткое и ясное содержание, "
        "призыв к действию. Вы должны максимально упростить жизнь клиенту "
        "и избегать длинных непонятных текстов. Не скатывайтесь в повествование, "
        "помните, что у каждого сообщения должна быть цель.",
    }

    def form_valid(self, form):
        """
        Автоматическое добавление текущего пользователям как создателя сообщения
        """
        if form.is_valid():
            self.object = form.save()
            user = self.request.user
            self.object.owner = user
            self.object.save()
            print(self.object)
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("email_newsletter:message")
    extra_context = {
        "title": "Здесь можно изменить сообщение для клиентов",
        "text": "Интересный заголовок, краткое и ясное содержание, "
        "призыв к действию. Вы должны максимально упростить жизнь клиенту "
        "и избегать длинных непонятных текстов. Не скатывайтесь в повествование, "
        "помните, что у каждого сообщения должна быть цель.",
    }

    def get_context_data(self, **kwargs):
        """
        Права доступа владельца.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner:
            return context_data
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("email_newsletter:message")
    extra_context = {
        "title": "Здесь можно удалить сообщение",
        "text": "Если больше не планируете клиентам направлять данное сообщение - "
        "то его можно удалить из Вашего Списка сообщений. .",
    }

    def get_context_data(self, **kwargs):
        """
        Права доступа владельца.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner:
            return context_data
        raise PermissionDenied


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    extra_context = {
        "title": "Вот как полностью выглядит сообщение",
        "text": "Интересный заголовок, краткое и ясное содержание, "
        "призыв к действию. Вы должны максимально упростить жизнь клиенту "
        "и избегать длинных непонятных текстов. Не скатывайтесь в повествование, "
        "помните, что у каждого сообщения должна быть цель.",
        "create_object": "Создать новое сообщение",
    }

    def get_context_data(self, **kwargs):
        """
        Права доступа владельца.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner:
            return context_data
        raise PermissionDenied


def homepage(request):
    """
    Главная страница
    """
    # количество сообщений
    count_mailings = Newsletter.objects.count()
    # количество активных сообщений
    count_mailings_is_active = len(Newsletter.objects.filter(is_active=True))
    # количество уникальных клиентов
    unique_clients = (
        Client.objects.all().values_list("email", flat=True).distinct().count()
    )
    # print(unique_clients)
    # три статьи для главной страницы
    random_blog_list = list(get_blog_from_cache())
    random.shuffle(random_blog_list)
    blog_list = random_blog_list[:3]
    # print(blog_list)
    context = {
        "title": "Вы попали на сайт создания рассылок",
        "text": "Вам требуется: во-первых, зарегистрироваться на сайте; "
        "во-вторых, создать либо загрузить базу клиентов, сообщений; "
        "в-третьих, создать рассылки для отправки сообщений определенным "
        "клиентам или даже всем... В итоге можете посмотреть отчет "
        "проведенных рассылок клиентам сообщений...",
        "blog_list": blog_list,
        "count_mailings": count_mailings,
        "count_mailings_is_active": count_mailings_is_active,
        "unique_clients": unique_clients,
    }
    return render(request, "email_newsletter/homepage.html", context)


@login_required
def get_mailing_report(request):
    """
    Отчет проведенных рассылок
    """
    user = request.user
    clients = Client.objects.all()
    newsletters = list(filter(lambda x: (x.owner == user), Newsletter.objects.all()))
    attempts = Attempt.objects.all().order_by("last_data")
    context = {
        "title": "Отчет проведенных рассылок",
        "text": "Отчет доставки отразит успешность отправки и доставки сообщений клиентам. "
        "С помощью отчета можно обнаружить, какие сообщения не доставлены, "
        "с установлением причины, "
        "а также оценить количество сообщений и процент успешно доставленных",
        "create_object": "Вернуться на главную",
        "clients": clients,
        "newsletters": newsletters,
        "attempts": attempts,
    }
    return render(request, "email_newsletter/mailing_report.html", context)
