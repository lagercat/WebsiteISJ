from django import forms

from captcha.fields import ReCaptchaField


class LoginForm(forms.Form):
    re_captcha = ReCaptchaField()

    username = forms.CharField(max_length=30, label="Nume de utilizator",
                               widget=forms.TextInput(attrs={
                                   'required': 'required',
                                   'placeholder': 'Nume de utilizator'
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
    new_password_check = forms.CharField(max_length=100, label="Introdu inca o data parola nou",
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
                raise forms.ValidationError("Parola noua nu se potriveste cu verificarea acesteia")
            elif not (any(x.isupper() for x in new_password) and any(x.islower() for x in new_password)
                      and any(x.isdigit() for x in new_password) and len(new_password) >= 8
                      and any(set(specials).intersection(x) for x in new_password)):
                raise forms.ValidationError("Parola trebuie ca aiba cel putin 8 caractere si sa contina cel"
                                            " putin: o litera mare, o litera mica, un numar si un caracter"
                                            " special")
