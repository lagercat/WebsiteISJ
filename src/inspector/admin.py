from django.contrib import admin

from models import Inspector


class InspectorAdmin(admin.ModelAdmin):
    list_display = ['user']
    ordering = ['user']

admin.site.register(Inspector, InspectorAdmin)