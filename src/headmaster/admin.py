from django.contrib import admin

from models import Headmaster


class HeadmasterAdmin(admin.ModelAdmin):
    list_display = ['user']
    ordering = ['user']

admin.site.register(Headmaster, HeadmasterAdmin)