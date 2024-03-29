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

from django_google_maps import widgets as map_widgets

from models import School
from utility.utility import clean_file


class SchoolCreationFormAdmin(forms.ModelForm):
    address = forms.CharField(widget=map_widgets.GoogleMapsAddressWidget())
    geolocation = forms.CharField(widget=forms.HiddenInput(), label='')

    class Meta:
        model = School
        fields = ('name', 'email', 'website', 'file', 'type_school',
                  'telephone', 'fax')

    def __init__(self, *args, **kwargs):
        super(SchoolCreationFormAdmin, self).__init__(*args, **kwargs)
        self.fields['telephone'].widget.attrs['placeholder'] = "+40735122139"
        self.fields['fax'].widget.attrs['placeholder'] = "+40735122139"

    def clean(self):
        cleaned_data = super(SchoolCreationFormAdmin, self).clean()
        try:
            geoloc = cleaned_data['geolocation']
            addr = cleaned_data['address']
            if geoloc == "Invalid address or no results":
                cleaned_data['geolocation'] = "0,0"
                cleaned_data['address'] = ""
                self.add_error("address", forms.ValidationError(
                    "The address is invalid"))
            if addr == "Invalid geolocation":
                cleaned_data['geolocation'] = "0,0"
                cleaned_data['address'] = ""
                self.add_error("address", forms.ValidationError(
                    "The geolocation is invalid"))
        except:
            cleaned_data['geolocation'] = "0,0"
            cleaned_data['address'] = ""
            self.add_error("address", forms.ValidationError(
                "The address is invalid"))
        if self.errors.get("geolocation"):
            del self.errors["geolocation"]
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(SchoolCreationFormAdmin, self).save(commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.address = self.cleaned_data['address']
        uploaded_file.geolocation = self.cleaned_data['geolocation']
        if commit:
            uploaded_file.save()
        return uploaded_file


class SchoolChangeFormAdmin(forms.ModelForm):
    address = forms.CharField(widget=map_widgets.GoogleMapsAddressWidget)
    geolocation = forms.CharField(widget=forms.HiddenInput(), label='')

    class Meta:
        model = School
        fields = ('name', 'email', 'website', 'file', 'type_school',
                  'telephone', 'fax')

    def __init__(self, *args, **kwargs):
        initial = {
            'address': self.address_initial,
            'geolocation': self.geolocation_initial,
        }
        kwargs['initial'] = initial
        super(SchoolChangeFormAdmin, self).__init__(*args, **kwargs)
        self.fields['telephone'].widget.attrs['placeholder'] = "+40735122139"
        self.fields['fax'].widget.attrs['placeholder'] = "+40735122139"

    def clean(self):
        cleaned_data = super(SchoolChangeFormAdmin, self).clean()
        try:
            geoloc = cleaned_data['geolocation']
            addr = cleaned_data['address']
            if geoloc == "Invalid address or no results":
                cleaned_data['address'] = self.address_initial
                cleaned_data['geolocation'] = self.geolocation_initial
                self.add_error("address", forms.ValidationError(
                    "The address is invalid"))
            if addr == "Invalid geolocation":
                cleaned_data['address'] = self.address_initial
                cleaned_data['geolocation'] = self.geolocation_initial
                self.add_error("geolocation", forms.ValidationError(
                    "The geolocation is invalid"))
        except:
            cleaned_data['address'] = self.address_initial
            cleaned_data['geolocation'] = self.geolocation_initial
            self.add_error("address", forms.ValidationError(
                "The address is invalid"))
        return cleaned_data

    def clean_file(self):

        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(SchoolChangeFormAdmin, self).save(commit=False)
        uploaded_file.address = self.cleaned_data['address']
        uploaded_file.geolocation = self.cleaned_data['geolocation']
        if commit:
            uploaded_file.save()
        return uploaded_file
