from django.contrib import admin
from models import School
from utility.admin import AdminChangeMixin, register_model_admin
from django import forms

from forms import SchoolCreationFormAdmin, SchoolChangeFormAdmin
from django.contrib.admin.filters import DateFieldListFilter


# Register your models here.

class SchoolAdmin(AdminChangeMixin):
    add_form = SchoolCreationFormAdmin
    change_form = SchoolChangeFormAdmin
    change_own_field = "id"
    change_own_owner_field = "school"

    icon = '<i class="material-icons">room</i>'

    list_display = ('name', 'telephone', 'fax', 'email', 'website', 'address',
                  'geolocation', 'file',)

    search_fields = (
        'name', 'address',)

    filter_horizontal = ()

    change_fieldsets = (
        ('School name', {'fields': ('name',)}),
        ('School Contact',
         {'fields': ('telephone', 'fax', 'email', 'website', 'file',)}),
        ('Location and Time', {'fields': ('address', 'geolocation',)}),
    )

    add_fieldsets = (
        ('School name', {'fields': ('name',)}),
        ('School Contact',
         {'fields': ('telephone', 'fax', 'email', 'website', 'file',)}),
        ('Location and Time', {'fields': ( 'address', 'geolocation',)}),
    )

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fieldsets = self.add_fieldsets
            form = self.add_form
            form.current_user = request.user
            return form
        else:
            self.fieldsets = self.change_fieldsets
            form = self.change_form
            form.address_initial = obj.address
            form.geolocation_initial = obj.geolocation
            return form

    pass


register_model_admin(School, SchoolAdmin)
