from django import forms

from django_google_maps import widgets as map_widgets
from models import School
from utility.utility import clean_file


class SchoolCreationFormAdmin(forms.ModelForm):
    address = forms.CharField(widget=map_widgets.GoogleMapsAddressWidget())
    geolocation = forms.CharField()

    class Meta:
        model = School
        fields = ('name', 'telephone', 'fax', 'email', 'website', 'address',
                  'geolocation', 'file',)

    def clean(self):
        cleaned_data = super(SchoolCreationFormAdmin, self).clean()
        geoloc = cleaned_data['geolocation']
        addr = cleaned_data['address']
        if geoloc == "Invalid address or no results":
            self.add_error("address",
                           forms.ValidationError("The address is invalid"))
        if addr == "Invalid geolocation":
            self.add_error("geolocation",
                           forms.ValidationError("The geolocation is invalid"))
        return cleaned_data

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(SchoolCreationFormAdmin, self).save(commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.address = self.cleaned_data['address']
        uploaded_file.geolocation = self.cleaned_data['geolocation']
        if commit:
            uploaded_file.save()
        return uploaded_file


class SchoolChangeFormAdmin(forms.ModelForm):
    address = forms.CharField(widget=map_widgets.GoogleMapsAddressWidget)
    geolocation = forms.CharField()

    class Meta:
        model = School
        fields = ('name', 'telephone', 'fax', 'email', 'website', 'address',
                  'geolocation', 'file',)

    def __init__(self, *args, **kwargs):
        initial = {
            'address': self.address_initial,
            'geolocation': self.geolocation_initial,
        }
        kwargs['initial'] = initial
        super(SchoolChangeFormAdmin, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SchoolChangeFormAdmin, self).clean()
        geoloc = cleaned_data['geolocation']
        addr = cleaned_data['address']
        if geoloc == "Invalid address or no results":
            self.add_error("address",
                           forms.ValidationError("The address is invalid"))
        if addr == "Invalid geolocation":
            self.add_error("geolocation",
                           forms.ValidationError("The geolocation is invalid"))
        return cleaned_data

    def clean_file(self):

        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(SchoolChangeFormAdmin, self).save(commit=False)
        uploaded_file.address = self.cleaned_data['address']
        uploaded_file.geolocation = self.cleaned_data['geolocation']
        if commit:
            uploaded_file.save()
        return uploaded_file
