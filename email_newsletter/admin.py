from django.contrib import admin

from email_newsletter.models import Client, Message, Newsletter, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_data', 'end_data', 'periodicity', 'status', 'message',)
    list_filter = ('client', 'message', 'status', 'periodicity',)
    # search_fields = ('product_name', 'description',)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_data', 'status', 'answer', 'newsletter',)
    list_filter = ('status', 'answer', 'newsletter',)
