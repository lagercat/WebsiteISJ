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

from gallery.models import Gallery, GalleryPhoto
from utility.utility import clean_file


class GalleryCreationFormAdmin(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = ('name', 'file')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(GalleryPhotoCreationForm,
                              self).save(commit=False)
        uploaded_file.author = self.current_author
        if commit:
            uploaded_file.save()
        return uploaded_file


class GalleryChangeFormAdmin(forms.ModelForm):
    gallery_photos = forms.CharField(
        label='', widget=forms.TextInput(attrs={"type": "hidden"}))
    gallery_photos_urls = forms.CharField(
        label='', widget=forms.TextInput(attrs={"type": "hidden"}))
    id = forms.CharField(
        label='', widget=forms.TextInput(attrs={"type": "hidden"}))

    class Meta:
        model = Gallery
        fields = ('name', 'file')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def __init__(self, *args, **kwargs):
        q = GalleryPhoto.objects.filter(gallery=kwargs["instance"]).extra(
            select={'order': 'CAST(name AS INTEGER)'}
        ).order_by('order')
        initial = {
            'gallery_photos': " ".join(
                list(str(gallery["id"]) for gallery in q.values("id"))),
            'gallery_photos_urls': " ".join(
                list(str(gallery["file"]) for gallery in q.values("file"))),
            'id': kwargs["instance"].id,
        }
        kwargs['initial'] = initial
        super(GalleryChangeFormAdmin, self).__init__(*args, **kwargs)


class GalleryPhotoCreationForm(forms.ModelForm):
    name = forms.CharField(label="Name")
    file = forms.FileField(label="File")

    class Meta:
        model = GalleryPhoto
        fields = ()

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(GalleryPhotoCreationForm,
                              self).save(commit=False)
        uploaded_file.file = self.cleaned_data['file']
        uploaded_file.name = self.cleaned_data['name']
        uploaded_file.gallery = self.gallery
        if commit:
            uploaded_file.save()
        return uploaded_file
