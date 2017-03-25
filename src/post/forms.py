import os

from django import forms
from django.forms import modelformset_factory

from models import Post, Page
from tinymce.widgets import TinyMCE, AdminTinyMCE
from utility.utility import clean_file

    
class PostCreationFormAdmin(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'file',)

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file
      
    def save(self, commit=True):
        uploaded_file = super(PostCreationFormAdmin, self).save(commit=False)
        if commit:
            uploaded_file.save()
        return uploaded_file


class PostChangeFormAdmin(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'file')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file
      
class PageCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_page/"
    
    class Meta:
        model = Page
        fields = ('name', 'file',)
        
    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(PageCreationFormAdmin, self).save(commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.text = self.cleaned_data['text']
        if commit:
            uploaded_file.save()
        return uploaded_file

class PageChangeFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_page/"
    
    class Meta:
        model = Page
        fields = ('name', 'file')
        
    def __init__(self, *args, **kwargs):
        initial = {
          'text': self.text_initial
        }
        kwargs['initial'] = initial
        super(PageChangeFormAdmin, self).__init__(*args, **kwargs)
        
    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file
      
    def save(self, commit=True):
        uploaded_file = super(PageChangeFormAdmin, self).save(commit=False)
        uploaded_file.text = self.cleaned_data['text']
        if commit:
            uploaded_file.save()
        return uploaded_file

PostFormSet = modelformset_factory(Post, form=PostCreationFormAdmin)