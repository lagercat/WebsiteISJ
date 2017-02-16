from django import forms
from django.db.models.fields import CharField
from gallery.models import Gallery, GalleryPhoto
import os
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
        uploaded_file = super(GalleryPhotoCreationForm, self).save(commit=False)
        uploaded_file.author= self.current_author
        if commit:
            uploaded_file.save()
        return uploaded_file
        

class GalleryChangeFormAdmin(forms.ModelForm):
    gallery_photos = forms.CharField(label='',  widget=forms.TextInput(attrs={"type": "hidden"}))
    gallery_photos_urls = forms.CharField(label='',  widget=forms.TextInput(attrs={"type": "hidden"}))
    id = forms.CharField(label='',  widget=forms.TextInput(attrs={"type": "hidden"}))
    
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
          'gallery_photos': " ".join(list(str(gallery["id"]) for gallery in q.values("id"))),
          'gallery_photos_urls': " ".join(list(str(gallery["file"]) for gallery in q.values("file"))),
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
        uploaded_file = super(GalleryPhotoCreationForm, self).save(commit=False)
        uploaded_file.file= self.cleaned_data['file']
        uploaded_file.name = self.cleaned_data['name']
        uploaded_file.gallery = self.gallery
        if commit:
            uploaded_file.save()
        return uploaded_file