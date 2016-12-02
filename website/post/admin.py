from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    list_display = ['filename']
    ordering = ['date']