from django.contrib import admin

from models import School
from utility.admin import AdminChangeMixin, register_model_admin


class SchoolAdmin(AdminChangeMixin):
    list_display = ['name']
    list_order = ['name']
    icon = '<i class="material-icons">location_city</i>'

register_model_admin(School, SchoolAdmin)