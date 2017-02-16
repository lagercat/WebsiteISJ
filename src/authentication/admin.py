'''
Created on Jan 6, 2017

@author: roadd
'''
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from forms import ExtendedUserChangeFormAdmin, ExtendedUserCreationFormAdmin

from models import ExtendedUser
from material.frontend import models

class ExtendedUserAdmin(BaseUserAdmin):
    form = ExtendedUserChangeFormAdmin
    add_form = ExtendedUserCreationFormAdmin

    icon = '<i class="material-icons">account_box</i>'
    
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'school', 'get_subjects',
                    'status', 'is_active')
    
    list_filter = ('is_admin',)
    fieldsets = (
        ('Login Information', {'fields': ('email', ('password1', 'password2'))}),
        ('Personal info', {'fields': (('first_name', 'last_name'), 'date_of_birth', 'phone_number', ('subjects', 'school'))}),
        ('Permissions', {'fields': ('is_active', 'status')}),
    )
    
    add_fieldsets = (
        ('Login Information', {'fields': ('email', ('password1', 'password2'))}),
        ('Personal info', {'fields': (('first_name', 'last_name'), 'date_of_birth', 'phone_number', ('subjects', 'school'))}),
        ('Permissions', {'fields': ('status',)}),
    )
    
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'school__name',)
    ordering = ('email', 'first_name', 'last_name', 'phone_number', 'school__name',)
    filter_horizontal = ()

    def get_subjects(self, obj):
        return "\n".join([p.name + "," for p in obj.subjects.all()])
      
    get_subjects.short_description = 'Subjects'
    
    def get_readonly_fields(self, request, obj=None):
        if obj == request.user:  # editing an existing object
            return self.readonly_fields + ('status',)
        return self.readonly_fields

admin.site.register(ExtendedUser, ExtendedUserAdmin)

admin.site.unregister(Group)
admin.site.unregister(models.Module)