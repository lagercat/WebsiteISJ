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

class ExtendedUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = ExtendedUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'school')

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
        if commit:
            user.save()
        return user


class ExtendedUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = ExtendedUser
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'school', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class ExtendedUserAdmin(BaseUserAdmin):
    form = ExtendedUserChangeForm
    add_form = ExtendedUserCreationForm

    icon = '<i class="material-icons">people</i>'
    
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'school', 'is_admin', 'is_active')
    
    list_filter = ('is_admin',)
    fieldsets = (
        ('Login Information', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (('first_name', 'last_name'), 'date_of_birth', 'phone_number')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    
    add_fieldsets = (
        ('Login Information', {'fields': ('email', ('password1', 'password2'))}),
        ('Personal info', {'fields': (('first_name', 'last_name'), 'date_of_birth', 'phone_number')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'school',)
    ordering = ('email', 'first_name', 'last_name', 'phone_number', 'school',)
    filter_horizontal = ()

admin.site.register(ExtendedUser, ExtendedUserAdmin)

admin.site.unregister(Group)