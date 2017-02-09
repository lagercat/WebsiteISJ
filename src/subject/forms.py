from django import forms

from models import SubjectPost
from models import Subject
import os
from tinymce.widgets import AdminTinyMCE


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
        post = super(SubjectPostChangeFormAdmin, self).save(commit=False)
        post.text = self.cleaned_data['text']
        if commit:
            post.save()
        return post