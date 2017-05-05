from django import forms

from news.models import News
from tinymce.widgets import AdminTinyMCE
from utility.utility import clean_file


class NewsCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    date = forms.SplitDateTimeField()
    show_files = True
    show_preview = True
    preview_url = "/preview_news/"
    
    class Meta:
        model = News
        fields = ('name', 'file')
        
    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(NewsCreationFormAdmin, self).save(commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.text = self.cleaned_data['text']
        uploaded_file.date = self.cleaned_data['date']
        if commit:
            uploaded_file.save()
        return uploaded_file


class NewsChangeFormAdmin(forms.ModelForm):
    date = forms.SplitDateTimeField()
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_news/"
    
    class Meta:
        model = News
        fields = ('name', 'file')
        
    def __init__(self, *args, **kwargs):
        initial = {
          'text': self.text_initial
        }
        kwargs['initial'] = initial
        super(NewsChangeFormAdmin, self).__init__(*args, **kwargs)
        
    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file
      
    def save(self, commit=True):
        uploaded_file = super(NewsChangeFormAdmin, self).save(commit=False)
        uploaded_file.text = self.cleaned_data['text']
        uploaded_file.date = self.cleaned_data['date']
        if commit:
            uploaded_file.save()
        return uploaded_file
