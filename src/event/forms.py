'''
Created on Jan 10, 2017

@author: roadd
'''
from django.forms import SplitDateTimeWidget
from event.models import Event
from django import forms
from tinymce.widgets import AdminTinyMCE
import os
      
class EventCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    date = forms.SplitDateTimeField()
    show_files = True
    show_preview = True
    preview_url = "/preview_event/"
    
    class Meta:
        model = Event
        fields = ('name', 'file', 'event_location')
        
    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        max_size = 10000000  # 10 MB
        filename, file_type = os.path.splitext(uploaded_file.name)
        allowed_file_types = [
            '.doc', '.docx', '.docm', '.xls', '.xlsx', '.ppt',
            '.ppt', '.pps', '.zip', '.rar', '.jpg', '.jpeg'
            '.png', '.gif', '.bmp', '.txt', '.tif', '.rtf', '.pdf',
            '.odt', '.ace', '.ods', '.odg'
        ]
        if not(any(file_type in type for type in allowed_file_types)):
            raise forms.ValidationError("Fisierul nu se incadreaza in extensile permise")
        if uploaded_file.size > max_size:
            raise forms.ValidationError("Fisierul trece de dimensiunea maxima de %d" % max_size)

        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(EventCreationFormAdmin, self).save(commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.text = self.cleaned_data['text']
        uploaded_file.date = self.cleaned_data['date']
        if commit:
            uploaded_file.save()
        return uploaded_file


class EventChangeFormAdmin(forms.ModelForm):
    date = forms.SplitDateTimeField()
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_event/"
    
    class Meta:
        model = Event
        fields = ('name', 'file',  'event_location')
        
    def __init__(self, *args, **kwargs):
        initial = {
          'text': self.text_initial
        }
        kwargs['initial'] = initial
        super(EventChangeFormAdmin, self).__init__(*args, **kwargs)
        
    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        max_size = 10000000  # 10 MB
        filename, file_type = os.path.splitext(uploaded_file.name)
        allowed_file_types = [
            '.doc', '.docx', '.docm', '.xls', '.xlsx', '.ppt',
            '.ppt', '.pps', '.zip', '.rar', '.jpg', '.jpeg'
            '.png', '.gif', '.bmp', '.txt', '.tif', '.rtf', '.pdf',
            '.odt', '.ace', '.ods', '.odg'
        ]
        if not(any(file_type in type for type in allowed_file_types)):
            raise forms.ValidationError("Fisierul nu se incadreaza in extensile permise")
        if uploaded_file.size > max_size:
            raise forms.ValidationError("Fisierul trece de dimensiunea maxima de %d" % max_size)

        return uploaded_file
      
    def save(self, commit=True):
        uploaded_file = super(EventChangeFormAdmin, self).save(commit=False)
        uploaded_file.text = self.cleaned_data['text']
        uploaded_file.date = self.cleaned_data['date']
        if commit:
            uploaded_file.save()
        return uploaded_file