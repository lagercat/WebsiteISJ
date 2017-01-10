from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from models import ExtendedUser

from captcha.fields import ReCaptchaField


class LoginForm(forms.Form):
    re_captcha = ReCaptchaField(
        attrs={'lang': 'ro'}
    )

    username = forms.CharField(max_length=30, label="Email",
                               widget=forms.TextInput(attrs={
                                   'required': 'required',
                                   'placeholder': 'Email'
                               }))
    password = forms.CharField(max_length=100, label="Parola",
                               widget=forms.PasswordInput(attrs={
                                   'required': 'required',
                                   'placeholder': 'Parola'
                               }))


class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(max_length=100, label="Parola veche",
                                   widget=forms.PasswordInput(attrs={
                                       'required': 'required',
                                       'placeholder': 'Parola veche'
                                   }))
    new_password = forms.CharField(max_length=100, label="Parola noua",
                                   widget=forms.PasswordInput(attrs={
                                       'required': 'required',
                                       'placeholder': 'Parola noua'
                                   }))
    new_password_check = forms.CharField(max_length=100,
                                         label="Introdu inca o data parola nou",
                                         widget=forms.PasswordInput(attrs={
                                             'required': 'required',
                                             'placeholder': 'Verifica parola noua'
                                         }))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        new_password_check = cleaned_data.get("new_password_check")
        specials = '[~!@#$%^&*()_+{}":;\']+$'
        if not (self.user.check_password(old_password)):
            raise forms.ValidationError("Parola veche nu este corecta")
        else:
            if not (new_password == new_password_check):
                raise forms.ValidationError(
                    "Parola noua nu se potriveste cu verificarea acesteia")
            elif not (any(x.isupper() for x in new_password) and any(
                    x.islower() for x in new_password)
                      and any(x.isdigit() for x in new_password) and len(
                new_password) >= 8
                      and any(
                    set(specials).intersection(x) for x in new_password)):
                raise forms.ValidationError(
                    "Parola trebuie ca aiba cel putin 8 caractere si sa contina cel"
                    " putin: o litera mare, o litera mica, un numar si un caracter"
                    " special")


class ExtendedUserCreationFormAdmin(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = ExtendedUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'school', 'subjects', 'status')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ExtendedUserCreationFormAdmin, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_admin = (user.status == 3)
        if commit:
            user.save()
        return user


class ExtendedUserChangeFormAdmin(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = ExtendedUser
        fields = (
        'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'school', 'is_active', 'subjects',
        'status')

    def clean_password(self):
        return self.initial["password"]

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ExtendedUserChangeFormAdmin, self).save(commit=False)
        user.is_admin = user.status == 3
        if commit:
            user.save()
        return user

