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
from django.core.validators import validate_email
from django.utils.datetime_safe import datetime

from captcha.fields import ReCaptchaField

from .models import Contact


class CreateContactForm(forms.ModelForm):
    captcha = ReCaptchaField(attrs={
        'lang': 'ro'})

    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput({'required': 'required',
                                       'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={'required': 'required',
                                             'placeholder': 'Message'})
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError("Introdu un prenume valid")
        return first_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if validate_email(email):
            raise forms.ValidationError("Introdu o adresa de email valida")
        return email

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError("Introdu un nume valid")
        return last_name

    def clean_message(self):
        email = self.cleaned_data['email']
        date = datetime.now().strftime('%d/%m/%Y')
        message = self.cleaned_data['message']
        if len(message) < 50:
            raise forms.ValidationError(
                "Mesajul tau e prea scurt "
                "Trebuie sa contina minim 50 de caractere")
        message = email + ' ' + date + '\n' + message
        print message
        return message
