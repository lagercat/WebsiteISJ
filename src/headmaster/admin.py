from django.contrib import admin

from models import Headmaster
from view_permission.admin import AdminViewMixin


class HeadmasterAdmin(AdminViewMixin):
    list_display = ['user']
    ordering = ['user']
    icon = '<i class="material-icons">event_seat</i>'

admin.site.register(Headmaster, HeadmasterAdmin)