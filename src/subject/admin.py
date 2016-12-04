from django.contrib import admin

from models import Subject


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']

admin.site.register(Subject, SubjectAdmin)
