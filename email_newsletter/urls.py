from django.urls import path

from email_newsletter.apps import EmailNewsletterConfig
from email_newsletter.views import (NewsletterListView, NewsletterCreateView, NewsletterUpdateView,
                                    NewsletterDeleteView, NewsletterDetailView, ClientListView, ClientCreateView,
                                    ClientUpdateView, ClientDeleteView, ClientDetailView, MessageListView,
                                    MessageCreateView, MessageUpdateView, MessageDeleteView, MessageDetailView,
                                    homepage, get_mailing_report
                                    )

app_name = EmailNewsletterConfig.name

urlpatterns = [
    path('', homepage, name='homepage'),

    path('newsletter/', NewsletterListView.as_view(), name='newsletter'),
    path('create_newsletter/', NewsletterCreateView.as_view(), name='create_newsletter'),
    path('update_newsletter/<int:pk>', NewsletterUpdateView.as_view(), name='update_newsletter'),
    path('delete_newsletter/<int:pk>', NewsletterDeleteView.as_view(), name='delete_newsletter'),
    path('view_newsletter/<int:pk>', NewsletterDetailView.as_view(), name='view_newsletter'),

    path('client/', ClientListView.as_view(), name='client'),
    path('client/create_client/', ClientCreateView.as_view(), name='create_client'),
    path('client/update_client/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('client/delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
    path('client/view_client/<int:pk>', ClientDetailView.as_view(), name='view_client'),

    path('message/', MessageListView.as_view(), name='message'),
    path('message/create_message/', MessageCreateView.as_view(), name='create_message'),
    path('message/update_message/<int:pk>', MessageUpdateView.as_view(), name='update_message'),
    path('message/delete_message/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
    path('message/view_message/<int:pk>', MessageDetailView.as_view(), name='view_message'),

    path('mailing_report/', get_mailing_report, name='mailing_report'),
]
