from django.contrib import admin

from .models import Client


class ClientModelAdmin(admin.ModelAdmin):
    filter_horizontal = ['resources']


admin.site.register(Client, ClientModelAdmin)
