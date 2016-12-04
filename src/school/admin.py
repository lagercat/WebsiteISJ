from django.contrib import admin

from models import School


class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_order = ['name']

admin.site.register(School, SchoolAdmin)