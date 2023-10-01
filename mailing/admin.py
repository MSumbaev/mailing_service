from django.contrib import admin

from mailing.models import Client, MailingMessage, MailingSettings


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name',)


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'message')
    search_fields = ('subject',)


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'message', 'period', 'start_time', 'end_time', 'status')
    search_fields = ('clients', 'message',)
