from django.contrib import admin

from models import Inspector
from view_permission.admin import AdminViewMixin


class InspectorAdmin(AdminViewMixin):
    list_display = ['user']
    ordering = ['user']
    icon = '<i class="material-icons">supervisor_account</i>'

admin.site.register(Inspector, InspectorAdmin)