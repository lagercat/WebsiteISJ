from django.contrib import admin

from models import Headmaster


class HeadmasterAdmin(admin.ModelAdmin):
    list_display = ['user']
    ordering = ['user']
    icon = '<i class="material-icons">event_seat</i>'

admin.site.register(Headmaster, HeadmasterAdmin)