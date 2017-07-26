from django import forms
from django.core.validators import validate_email

from captcha.fields import ReCaptchaField

from .models import Contact


class CreateContactForm(forms.ModelForm):
    captcha = ReCaptchaField(attrs={
        'lang': 'ro'})

    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput({'required': 'required',
                                       'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={'required': 'required',
                                             'placeholder': 'Message'})
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError("Introdu un prenume valid")
        return first_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if validate_email(email):
            raise forms.ValidationError("Introdu o adresa de email valida")
        return email

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError("Introdu un nume valid")
        return last_name

    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 50:
            raise forms.ValidationError(
                "Mesajul tau e prea scurt "
                "Trebuie sa contina minim 50 de caractere")
        return message
