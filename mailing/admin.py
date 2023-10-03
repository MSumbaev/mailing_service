from django.contrib import admin

from mailing.models import Client, MailingMessage, MailingSettings, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name',)


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'message' 'owner')
    search_fields = ('subject', 'owner')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'message', 'period', 'clients', 'status', 'owner',)
    list_filter = ('clients', 'status', 'period', 'message', 'owner',)
    search_fields = ('clients', 'message', 'owner',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_try', 'status', 'client',)
    list_filter = ('client', 'status',)
    search_fields = ('client', 'status')
