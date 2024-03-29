# Copyright 2017 Adrian-Ioan Garovat, Emanuel Covaci, Sebastian-Valeriu Males
#
# This file is part of WebsiteISJ
#
# WebsiteISJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebsiteISJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from forms import ExtendedUserChangeFormAdmin
from forms import ExtendedUserCreationFormAdmin
from material.frontend import models
from models import ExtendedUser
from utility.admin import register_module_admin


class ExtendedUserAdmin(BaseUserAdmin):
    form = ExtendedUserChangeFormAdmin
    add_form = ExtendedUserCreationFormAdmin

    icon = '<i class="material-icons">account_box</i>'

    list_display = ('username', 'first_name', 'last_name', 'school',
                    'get_subjects', 'status', 'is_active')

    list_filter = ('is_admin', 'status')
    fieldsets = (
        ('Login Information', {
         'fields': ('username', ('password1', 'password2'))}),
        ('Personal info', {
         'fields': (('first_name', 'last_name'), ('subjects', 'school'))}),
        ('Permissions', {'fields': ('is_active', 'status')}),
    )

    add_fieldsets = (
        ('Login Information', {
         'fields': ('username', ('password1', 'password2'))}),
        ('Personal info', {
         'fields': (('first_name', 'last_name'), ('subjects', 'school'))}),
        ('Permissions', {'fields': ('status',)}),
    )

    search_fields = ('username', 'first_name', 'last_name', 'school__name',)
    ordering = ('username', 'first_name', 'last_name', 'school__name',)
    filter_horizontal = ()

    def get_subjects(self, obj):
        return "\n".join([p.name + "," for p in obj.subjects.all()])

    get_subjects.short_description = 'Subjects'

    def get_readonly_fields(self, request, obj=None):
        if obj == request.user:  # editing an existing object
            return self.readonly_fields + ('status',)
        return self.readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super(ExtendedUserAdmin, self).get_form(request, obj, **kwargs)
        if obj is not None:
            form.status_initial = obj.status
        return form


admin.site.register(ExtendedUser, ExtendedUserAdmin)
admin.site.unregister(Group)
admin.site.unregister(models.Module)
register_module_admin()
