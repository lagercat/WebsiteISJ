from django import forms

from models import SubjectPost
from models import Subject
import os
from tinymce.widgets import AdminTinyMCE
from utility.utility import clean_file


class SubjectPostCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_subjectpost/"
    
    class Meta:
        model = SubjectPost
        fields = ('name', 'subject', 'file')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        post = super(SubjectPostCreationFormAdmin, self).save(commit=False)
        post.author = self.current_user
        post.text = self.cleaned_data['text']
        if commit:
            post.save()
        return post


class SubjectPostChangeFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_subjectpost/"
    
    class Meta:
        model = SubjectPost
        fields = ('name', 'file')
    
    def __init__(self, *args, **kwargs):
        initial = {
          'text': self.text_initial
        }
        kwargs['initial'] = initial
        super(SubjectPostChangeFormAdmin, self).__init__(*args, **kwargs)
    
    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file
      
    def save(self, commit=True):
        post = super(SubjectPostChangeFormAdmin, self).save(commit=False)
        post.text = self.cleaned_data['text']
        if commit:
            post.save()
        return post