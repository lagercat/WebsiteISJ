from django.contrib import admin

from models import School
from view_permission.admin import AdminViewMixin


class SchoolAdmin(AdminViewMixin):
    list_display = ['name']
    list_order = ['name']
    icon = '<i class="material-icons">location_city</i>'

admin.site.register(School, SchoolAdmin)