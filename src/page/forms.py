from django import forms
from page.models import Article, SimplePage
from tinymce.widgets import AdminTinyMCE
import os
from utility.utility import clean_file


class ArticleCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
                           label='')
    date = forms.SplitDateTimeField()
    show_files = True
    show_preview = True
    preview_url = "/preview_news/"

    class Meta:
        model = Article
        fields = ('subcategory', 'name', 'file')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(ArticleCreationFormAdmin, self).save(
            commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.text = self.cleaned_data['text']
        uploaded_file.date = self.cleaned_data['date']
        if commit:
            uploaded_file.save()
        return uploaded_file


class ArticleChangeFormAdmin(forms.ModelForm):
    date = forms.SplitDateTimeField()
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
                           label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_news/"

    class Meta:
        model = Article
        fields = ('subcategory', 'name', 'file')

    def __init__(self, *args, **kwargs):
        initial = {
            'text': self.text_initial
        }
        kwargs['initial'] = initial
        super(ArticleChangeFormAdmin, self).__init__(*args, **kwargs)

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(ArticleChangeFormAdmin, self).save(commit=False)
        uploaded_file.text = self.cleaned_data['text']
        uploaded_file.date = self.cleaned_data['date']
        if commit:
            uploaded_file.save()
        return uploaded_file


class SimplePageCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(
        widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
        label='')
    date = forms.SplitDateTimeField()
    show_files = True
    show_preview = True
    preview_url = "/preview_news/"

    class Meta:
        model = SimplePage
        fields = ('category', 'name', 'file')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(SimplePageCreationFormAdmin, self).save(
            commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.text = self.cleaned_data['text']
        uploaded_file.date = self.cleaned_data['date']
        if commit:
            uploaded_file.save()
        return uploaded_file


class SimplePageChangeFormAdmin(forms.ModelForm):
    date = forms.SplitDateTimeField()
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
                           label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_news/"

    class Meta:
        model = SimplePage
        fields = ('category', 'name', 'file')

    def __init__(self, *args, **kwargs):
        initial = {
            'text': self.text_initial
        }
        kwargs['initial'] = initial
        super(SimplePageChangeFormAdmin, self).__init__(*args, **kwargs)

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(SimplePageChangeFormAdmin, self).save(
            commit=False)
        uploaded_file.text = self.cleaned_data['text']
        uploaded_file.date = self.cleaned_data['date']
        if commit:
            uploaded_file.save()
        return uploaded_file
