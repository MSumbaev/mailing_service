import mailing.apps
from django.urls import path

from mailing.views import index, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, MessageListView, \
    MessageCreateView, MessageUpdateView, MessageDeleteView, MailingSettingsListView, MailingSettingsCreateView, \
    MailingSettingsUpdateView, MailingSettingsDeleteView, toggle_status

app_name = mailing.apps.MailingConfig.name

urlpatterns = [
    path('', index, name='index'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailings/', MailingSettingsListView.as_view(), name='mailing_list'),
    path('mailings_create/', MailingSettingsCreateView.as_view(), name='mailing_create'),
    path('mailings_update/<int:pk>/', MailingSettingsUpdateView.as_view(), name='mailing_update'),
    path('mailings_delete/<int:pk>/', MailingSettingsDeleteView.as_view(), name='mailing_delete'),
    path('toggle_status/<int:pk>/', toggle_status, name='toggle_status'),
]
