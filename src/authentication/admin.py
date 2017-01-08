'''
Created on Jan 6, 2017

@author: roadd
'''

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from models import ExtendedUser
from material.frontend import models


class ExtendedUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = ExtendedUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'school', 'subjects', 'status')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ExtendedUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_admin = (user.status == 3)
        if commit:
            user.save()
        return user


class ExtendedUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = ExtendedUser
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'school', 'is_active', 'subjects', 'status')

    def clean_password(self):
        return self.initial["password"]
      
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ExtendedUserChangeForm, self).save(commit=False)
        user.is_admin = user.status == 3
        if commit:
            user.save()
        return user


class ExtendedUserAdmin(BaseUserAdmin):
    form = ExtendedUserChangeForm
    add_form = ExtendedUserCreationForm

    icon = '<i class="material-icons">account_box</i>'
    
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'school', 'get_subjects',
                    'status', 'is_active')
    
    list_filter = ('is_admin',)
    fieldsets = (
        ('Login Information', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (('first_name', 'last_name'), 'date_of_birth', 'phone_number', 'subjects')}),
        ('Permissions', {'fields': ('is_active', 'status')}),
    )
    
    add_fieldsets = (
        ('Login Information', {'fields': ('email', ('password1', 'password2'))}),
        ('Personal info', {'fields': (('first_name', 'last_name'), 'date_of_birth', 'phone_number', 'subjects')}),
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