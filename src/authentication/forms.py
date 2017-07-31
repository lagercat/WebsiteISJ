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
from django import forms

from captcha.fields import ReCaptchaField
from models import ExtendedUser
from subject.models import Subject
from utility.forms import SelectWithDisabled


class LoginForm(forms.Form):
    re_captcha = ReCaptchaField(
        attrs={'lang': 'ro',
               'required': 'required'}
    )

    username = forms.CharField(max_length=150, label="username",
                               widget=forms.TextInput(attrs={
                                   'required': 'required',
                                   'placeholder': 'username'
                               }))
    password = forms.CharField(max_length=100, label="Parola",
                               widget=forms.PasswordInput(attrs={
                                   'required': 'required',
                                   'placeholder': 'Parola'
                               }))


class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(max_length=100, label="Parola veche",
                                   widget=forms.PasswordInput(attrs={
                                       'required': 'required',
                                       'placeholder': 'Parola veche'
                                   }))
    new_password = forms.CharField(max_length=100, label="Parola noua",
                                   widget=forms.PasswordInput(attrs={
                                       'required': 'required',
                                       'placeholder': 'Parola noua'
                                   }))
    new_password_check = forms.CharField(max_length=100,
                                         label="Introdu inca o"
                                         " data parola nou",
                                         widget=forms.PasswordInput(attrs={
                                             'required': 'required',
                                             'placeholder':
                                             'Verifica parola noua'
                                         }))


class ExtendedUserCreationFormAdmin(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)
    subjects = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={"multiple": "multiple"}),
        queryset=Subject.objects.all(), required=False)
    status = forms.ChoiceField(choices=(
        (0, "Personal"),
        (1, "Director"),
        (2, "Inspector"),
        (3, {"label": "Admin", "disabled": True}),
    ), required=True, label="User status", widget=SelectWithDisabled,
        initial=0)

    class Meta:
        model = ExtendedUser
        fields = ('first_name', 'last_name', 'username', 'school')

    def clean(self):
        data = self.cleaned_data
        status = data.get("status")
        status = int(status)
        if status in [0, 2, 3] and data.get("school"):
            raise forms.ValidationError(
                "School should be completed for directors only")
        if status == 1 and not data.get("school"):
            raise forms.ValidationError("Please choose a school for director")
        if status in [0, 1, 3] and data.get("subjects"):
            raise forms.ValidationError(
                "Subject should be completed for inspectors only")
        if status == 2 and not data.get("subjects"):
            raise forms.ValidationError(
                "Please choose a subject for inspector")
        return data

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ExtendedUserCreationFormAdmin, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_admin = (user.status == 3)
        user.save()
        for item in self.cleaned_data["subjects"]:
            user.subjects.add(item)
        if commit:
            user.save()
        return user


class ExtendedUserChangeFormAdmin(forms.ModelForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput,
        required=False)
    subjects = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={"multiple": "multiple"}),
        queryset=Subject.objects.all(), required=False)

    status = forms.ChoiceField(choices=(
        (0, "Personal"),
        (1, "Director"),
        (2, "Inspector"),
        (3,  {'label': "Admin", 'disabled': True}),
    ), required=True, label="User status", widget=SelectWithDisabled)

    class Meta:
        model = ExtendedUser
        fields = ('username', 'first_name',
                  'last_name', 'school', 'is_active')

    def __init__(self, *args, **kwargs):
        initial = {
            'status': self.status_initial
        }
        kwargs['initial'] = initial
        super(ExtendedUserChangeFormAdmin, self).__init__(*args, **kwargs)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean(self):
        data = self.cleaned_data
        data_changed = self.changed_data
        status = data.get(
            "status") if "status" in data_changed else self.instance.status
        school = data.get(
            "school") if "school" in data_changed else self.instance.school
        subjects = data.get("subjects")
        status = int(status)
        if status in [0, 2, 3] and school:
            raise forms.ValidationError(
                "School should be completed for directors only")
        if status == 1 and not school:
            raise forms.ValidationError("Please choose a school for director")
        if status in [0, 1, 3] and subjects:
            raise forms.ValidationError(
                "Subject should be completed for inspectors only")
        if status == 2 and not subjects:
            raise forms.ValidationError(
                "Please choose a subject for inspector")
        return data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ExtendedUserChangeFormAdmin, self).save(commit=False)
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        user.is_admin = user.status == 3
        if commit:
            user.save()
        for item in self.cleaned_data["subjects"]:
            user.subjects.add(item)
        if commit:
            user.save()
        return user
