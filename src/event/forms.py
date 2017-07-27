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
from datetime import datetime
from django import forms

from django_google_maps import widgets as map_widgets
from event.models import Event
from tinymce.widgets import AdminTinyMCE
from utility.utility import clean_file


class EventCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    date = forms.SplitDateTimeField()
    address = forms.CharField(widget=map_widgets.GoogleMapsAddressWidget())
    geolocation = forms.CharField(widget=forms.HiddenInput(), label='')

    show_files = True
    show_preview = True
    preview_url = "/preview_event/"

    class Meta:
        model = Event
        fields = ('name', 'file',)

    def clean(self):
        cleaned_data = super(EventCreationFormAdmin, self).clean()
        try:
            geoloc = cleaned_data['geolocation']
            addr = cleaned_data['address']
            if geoloc == "Invalid address or no results":
                self.add_error("address", forms.ValidationError("The address is invalid"))
            if addr == "Invalid geolocation":
                self.add_error("geolocation", forms.ValidationError("The geolocation is invalid"))
        except:
            self.add_error("address", forms.ValidationError("The address is invalid"))

        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def clean_date(self):
        data = self.cleaned_data['date']
        now = datetime.now()
        data = data.replace(tzinfo=None)
        if data < now:
            raise forms.ValidationError("Data nu e valida.Nu puteti posta un eveniment in trecut!")
        return data

    def save(self, commit=True):
        uploaded_file = super(EventCreationFormAdmin, self).save(commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.text = self.cleaned_data['text']
        uploaded_file.date = self.cleaned_data['date']
        uploaded_file.address = self.cleaned_data['address']
        uploaded_file.geolocation = self.cleaned_data['geolocation']
        if commit:
            uploaded_file.save()
        return uploaded_file


class EventChangeFormAdmin(forms.ModelForm):
    date = forms.SplitDateTimeField()
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    address = forms.CharField(widget=map_widgets.GoogleMapsAddressWidget)
    geolocation = forms.CharField()

    show_files = True
    show_preview = True
    preview_url = "/preview_event/"

    class Meta:
        model = Event
        fields = ('name', 'file')

    def __init__(self, *args, **kwargs):
        initial = {
          'text': self.text_initial,
          'date': self.date_initial,
          'address': self.address_initial,
          'geolocation': self.geolocation_initial,
        }
        kwargs['initial'] = initial
        super(EventChangeFormAdmin, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(EventChangeFormAdmin, self).clean()
        geoloc = cleaned_data['geolocation']
        addr = cleaned_data['address']
        if geoloc == "Invalid address or no results":
            self.add_error("address", forms.ValidationError("The address is invalid"))
        if addr == "Invalid geolocation":
            self.add_error("geolocation", forms.ValidationError("The geolocation is invalid"))
        return cleaned_data

    def clean_file(self):

        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def clean_date(self):
        data = self.cleaned_data['date']
        now = datetime.now()
        data = data.replace(tzinfo=None)
        if data < now:
            raise forms.ValidationError("Data nu e valida.Nu puteti posta un eveniment in trecut!")
        return data

    def save(self, commit=True):
        uploaded_file = super(EventChangeFormAdmin, self).save(commit=False)
        uploaded_file.text = self.cleaned_data['text']
        uploaded_file.date = self.cleaned_data['date']
        uploaded_file.address = self.cleaned_data['address']
        uploaded_file.geolocation = self.cleaned_data['geolocation']
        if commit:
            uploaded_file.save()
        return uploaded_file
