from django.contrib import admin

from service.models import Client, MailingSetup, Messages, Logs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_name', 'first_name', 'email', 'owner')
    list_filter = ('last_name', 'email', 'owner')
    search_fields = ('last_name', 'email', 'owner')


@admin.register(MailingSetup)
class MailingSetupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'data_begin', 'data_end', 'period', 'owner')
    list_filter = ('owner', )
    search_fields = ('owner', )


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'owner')
    list_filter = ('owner', )
    search_fields = ('owner', )


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'client', 'data_send', 'is_done')
    list_filter = ('client', )
    search_fields = ('client', )
