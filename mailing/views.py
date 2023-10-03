from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MessageForm, MailingSettingsForm
from mailing.models import Client, MailingMessage, MailingSettings, MailingLog


class GetObjectOwnerMixin:
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404

        return self.object


class GetQuerysetOwnerMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_staff is False:
            queryset = queryset.filter(owner=self.request.user)

        return queryset


class FormValidOwnerMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


def index(request):
    return render(request, 'mailing/index.html')


@login_required
@permission_required('mailing_list.set_status')
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
class ClientListView(LoginRequiredMixin, GetQuerysetOwnerMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты'
    }


class ClientCreateView(LoginRequiredMixin, FormValidOwnerMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(LoginRequiredMixin, GetObjectOwnerMixin, FormValidOwnerMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(LoginRequiredMixin, GetObjectOwnerMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


# ----------Сообщения----------
class MessageListView(LoginRequiredMixin, GetQuerysetOwnerMixin, ListView):
    model = MailingMessage
    extra_context = {
        'title': 'Список сообщений'
    }


class MessageCreateView(LoginRequiredMixin, FormValidOwnerMixin, CreateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(LoginRequiredMixin, GetObjectOwnerMixin, FormValidOwnerMixin, UpdateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(LoginRequiredMixin, GetObjectOwnerMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:message_list')


# ----------Рассылки----------
class MailingSettingsListView(LoginRequiredMixin, GetQuerysetOwnerMixin, ListView):
    model = MailingSettings
    extra_context = {
        'title': 'Список рассылок'
    }


class MailingSettingsCreateView(LoginRequiredMixin, FormValidOwnerMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['message'].queryset = MailingMessage.objects.filter(owner=self.request.user)
        form.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)

        return form


class MailingSettingsUpdateView(LoginRequiredMixin, GetObjectOwnerMixin, FormValidOwnerMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingSettingsDeleteView(LoginRequiredMixin, GetObjectOwnerMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')


class MailingLogListView(ListView, PermissionRequiredMixin):
    model = MailingLog
    permission_required = 'mailing.view_mailinglog'
    extra_context = {
        'title': 'Логи'
    }
