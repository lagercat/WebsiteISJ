from django import forms


class LoginForm(forms.Form):
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
