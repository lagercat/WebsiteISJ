'''
Created on Jan 10, 2017

@author: roadd
'''
from django.forms import SplitDateTimeWidget
from event.models import Event
from django import forms
from tinymce.widgets import AdminTinyMCE
import os
from django_google_maps import fields as map_fields
from django_google_maps import widgets as map_widgets
from utility.utility import clean_file
      
class EventCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    date = forms.SplitDateTimeField()
    address = forms.CharField(widget=map_widgets.GoogleMapsAddressWidget())
    geolocation = forms.CharField()
    
    show_files = True
    show_preview = True
    preview_url = "/preview_event/"
    class Meta:
        model = Event
        fields = ('name', 'file',)
        
    def clean(self):
        cleaned_data = super(EventCreationFormAdmin, self).clean()
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
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),label='')
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
      
    def save(self, commit=True):
        uploaded_file = super(EventChangeFormAdmin, self).save(commit=False)
        uploaded_file.text = self.cleaned_data['text']
        uploaded_file.date = self.cleaned_data['date']
        uploaded_file.address = self.cleaned_data['address']
        uploaded_file.geolocation = self.cleaned_data['geolocation']
        if commit:
            uploaded_file.save()
        return uploaded_file