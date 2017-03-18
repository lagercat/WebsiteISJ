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
from utility.admin import register_module_admin, register_module_admin
from material.frontend.admin import ModuleAdmin

class ExtendedUserAdmin(BaseUserAdmin):
    form = ExtendedUserChangeFormAdmin
    add_form = ExtendedUserCreationFormAdmin

    icon = '<i class="material-icons">account_box</i>'
    
    list_display = ('username', 'first_name', 'last_name', 'school', 'get_subjects',
                    'status', 'is_active')
    
    list_filter = ('is_admin',)
    fieldsets = (
        ('Login Information', {'fields': ('username', ('password1', 'password2'))}),
        ('Personal info', {'fields': (('first_name', 'last_name'), ('subjects', 'school'))}),
        ('Permissions', {'fields': ('is_active', 'status')}),
    )
    
    add_fieldsets = (
        ('Login Information', {'fields': ('username', ('password1', 'password2'))}),
        ('Personal info', {'fields': (('first_name', 'last_name'), ('subjects', 'school'))}),
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

admin.site.register(ExtendedUser, ExtendedUserAdmin)

admin.site.unregister(Group)
admin.site.unregister(models.Module)
register_module_admin()