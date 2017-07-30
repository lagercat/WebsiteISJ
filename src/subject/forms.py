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
from operator import or_

from django import forms
from django.db.models.query_utils import Q

from models import Subcategory
from models import SubjectPost
from tinymce.widgets import AdminTinyMCE
from utility.utility import clean_file


class SubjectPostCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
                           label='')

    show_files = True
    show_preview = True
    preview_url = "/preview_subjectpost/"

    class Meta:
        model = SubjectPost
        fields = ('name', 'subcategory', 'subject', 'file')

    def __init__(self, *args, **kwargs):
        super(SubjectPostCreationFormAdmin, self).__init__(*args, **kwargs)
        user = self.current_user
        if user.status is 2:
            self.fields['subject'].queryset = user.subjects.all()

            self.fields['subcategory'].queryset = Subcategory.objects.filter(
                reduce(or_, [Q(subject=s) for s in user.subjects.all()]))

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def clean_subject(self):
        subject = self.cleaned_data.get("subject")
        subcategory = self.cleaned_data.get("subcategory")
        if (subcategory is not None and subject is not None
                and subject != subcategory.subject):
            raise forms.ValidationError(
                "This should be empty or same subject as the subcategory")
        if subcategory is None and subject is None:
            raise forms.ValidationError("This should be not be empty")
        return self.cleaned_data.get("subject")

    def save(self, commit=True):
        post = super(SubjectPostCreationFormAdmin, self).save(commit=False)
        post.author = self.current_user
        post.text = self.cleaned_data['text']
        post.subject = self.cleaned_data[
            "subject"] or self.cleaned_data["subcategory"].subject
        if commit:
            post.save()
        return post


class SubjectPostChangeFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
                           label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_subjectpost/"

    class Meta:
        model = SubjectPost
        fields = ('name', 'file', 'subject', 'subcategory')

    def __init__(self, *args, **kwargs):
        initial = {
            'text': self.text_initial
        }
        kwargs['initial'] = initial
        super(SubjectPostChangeFormAdmin, self).__init__(*args, **kwargs)
        user = self.current_user
        if user.status is 2:
            self.fields['subject'].queryset = user.subjects.all()

            self.fields['subcategory'].queryset = Subcategory.objects.filter(
                reduce(or_, [Q(subject=s) for s in user.subjects.all()]))

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def clean_subject(self):
        subject = self.cleaned_data.get(
            "subject") if "subject" in self.changed_data else self.instance.subject
        subcategory = self.cleaned_data.get(
            "subcategory") if "subcategory" in self.changed_data else self.instance.subcategory
        if subcategory is not None and subject is not None and subject is not subcategory.subject:
            raise forms.ValidationError(
                "This should be empty or same subject as the subcategory")
        if subcategory is None and subject is None:
            raise forms.ValidationError("This should be not be empty")
        return self.cleaned_data.get("subject")

    def save(self, commit=True):
        post = super(SubjectPostChangeFormAdmin, self).save(commit=False)
        post.text = self.cleaned_data['text']
        post.subject = self.cleaned_data[
            "subject"] or self.cleaned_data["subcategory"].subject
        if commit:
            post.save()
        return post


class SubcategoryCreationFormAdmin(forms.ModelForm):

    class Meta:
        model = Subcategory
        fields = ('name', 'file', 'subject',)

    def __init__(self, *args, **kwargs):
        super(SubcategoryCreationFormAdmin, self).__init__(*args, **kwargs)
        user = self.current_user
        if user.status is 2:
            self.fields['subject'].queryset = user.subjects.all()

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(SubcategoryCreationFormAdmin,
                              self).save(commit=False)
        uploaded_file.author = self.current_user
        if commit:
            uploaded_file.save()
        return uploaded_file


class SubcategoryChangeFormAdmin(forms.ModelForm):

    class Meta:
        model = Subcategory
        fields = ('name', 'file', 'subject')

    def __init__(self, *args, **kwargs):
        super(SubcategoryChangeFormAdmin, self).__init__(*args, **kwargs)
        user = self.current_user
        if user.status is 2:
            self.fields['subject'].queryset = user.subjects.all()

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(SubcategoryChangeFormAdmin,
                              self).save(commit=False)
        if commit:
            uploaded_file.save()
        return uploaded_file
