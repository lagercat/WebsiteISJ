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
from .models import Registration
from tinymce.widgets import AdminTinyMCE
from utility.utility import clean_file


class RegistrationCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
                           label='')
    show_files = True
    show_preview = False

    class Meta:
        model = Registration
        fields = ('name', 'text','file', 'type_registration')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(RegistrationCreationFormAdmin, self).save(
            commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.text = self.cleaned_data['text']
        if commit:
            uploaded_file.save()
        return uploaded_file


class RegistrationChangeFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
                           label='')
    show_files = False
    show_preview = False

    class Meta:
        model = Registration
        fields = ('name','text','file', 'type_registration')

    def __init__(self, *args, **kwargs):
        super(RegistrationChangeFormAdmin, self).__init__(*args, **kwargs)

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(RegistrationChangeFormAdmin, self).save(commit=False)
        uploaded_file.text = self.cleaned_data['text']
        if commit:
            uploaded_file.save()
        return uploaded_file
