from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MessageForm, MailingSettingsForm
from mailing.models import Client, MailingMessage, MailingSettings


def index(request):
    return render(request, 'mailing/index.html')


def toggle_status(request, pk):
    """Контроллер для смены статуса рассылки"""
    mailing = MailingSettings.objects.get(pk=pk)
    if mailing.status == MailingSettings.STARTED:
        mailing.status = MailingSettings.DONE
    elif mailing.status == MailingSettings.DONE:
        mailing.status = MailingSettings.STARTED
    else:
        mailing.status = MailingSettings.STARTED
    mailing.save()
    return redirect('mailing:mailing_list')


# ----------Клиенты----------
class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты'
    }


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


# ----------Сообщения----------
class MessageListView(ListView):
    model = MailingMessage
    extra_context = {
        'title': 'Список сообщений'
    }


class MessageCreateView(CreateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(UpdateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:message_list')


# ----------Рассылки----------
class MailingSettingsListView(ListView):
    model = MailingSettings
    extra_context = {
        'title': 'Список рассылок'
    }


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')
