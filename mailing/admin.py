from django.contrib import admin

from mailing.models import Client, MailingMessage, MailingSettings, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name',)


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'message',)
    search_fields = ('subject', 'owner')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'message', 'period', 'status',)
    list_filter = ('clients', 'status', 'period', 'message',)
    search_fields = ('clients', 'message',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_try', 'status', 'client',)
    list_filter = ('client', 'status',)
    search_fields = ('client', 'status')
