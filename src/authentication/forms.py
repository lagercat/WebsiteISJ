from django import forms

from captcha.fields import ReCaptchaField
from models import ExtendedUser
from subject.models import Subject
from utility.forms import SelectWithDisabled
from nltk.app.nemo_app import initialFind

class LoginForm(forms.Form):
    re_captcha = ReCaptchaField(
        attrs={'lang': 'ro',
               'required':'required'}
    )

    username = forms.CharField(max_length=30, label="username",
                               widget=forms.TextInput(attrs={
                                   'required': 'required',
                                   'placeholder': 'username'
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


class ExtendedUserCreationFormAdmin(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    subjects = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={"multiple": "multiple"}),
                                              queryset=Subject.objects.all(), required=False)
    status = forms.ChoiceField(choices=(
        (0, "Personal"),
        (1, "Director"),
        (2, "Inspector"),
        (3, {"label": "Admin", "disabled": True}),
    ), required=True, label="User status", widget=SelectWithDisabled, initial=0)
    
    
    class Meta:
        model = ExtendedUser
        fields = ('first_name', 'last_name', 'username', 'school',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def clean_school(self):
        status = self.cleaned_data.get("status")
        if status in [0, 2, 3] and self.cleaned_data.get("school"):
            raise forms.ValidationError("This should be completed for directors only")
        if status == 1 and not self.cleaned_data.get("school"):
            raise forms.ValidationError("Please choose a school for director")
        return self.cleaned_data.get("school")
        
    def clean_subjects(self):
        status = self.cleaned_data.get("status")
        if status in [0, 1, 3] and self.cleaned_data.get("subjects"):
            raise forms.ValidationError("This should be completed for inspectors only")
        if status == 2 and not self.cleaned_data.get("subjects"):
            raise forms.ValidationError("Please choose a subject for inspector")
        return self.cleaned_data.get("subjects")
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ExtendedUserCreationFormAdmin, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_admin = (user.status == 3)
        user.save()
        for item in self.cleaned_data["subjects"]:
            user.subjects.add(item)
        if commit:
            user.save()
        return user


class ExtendedUserChangeFormAdmin(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)
    subjects = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={"multiple": "multiple"}),
                                              queryset=Subject.objects.all(), required=False)

    status = forms.ChoiceField(choices=(
        (0, "Personal"),
        (1, "Director"),
        (2, "Inspector"),
        (3,  {'label': "Admin", 'disabled': True}),
    ), required=True, label="User status", widget=SelectWithDisabled)

    class Meta:
        model = ExtendedUser
        fields = ('username', 'first_name', 'last_name', 'school', 'is_active', )
        
    def __init__(self, *args, **kwargs):
        initial = {
            'status': self.status_initial
        }
        kwargs['initial'] = initial
        super(ExtendedUserChangeFormAdmin, self).__init__(*args, **kwargs)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_school(self):
        status = self.cleaned_data.get("status") if "status" in self.changed_data else self.instance.status
        school = self.cleaned_data.get("school") if "school" in self.changed_data else self.instance.school
        if status in [0, 2, 3] and school:
            raise forms.ValidationError("This should be completed for directors only")
        if status == 1 and not school:
            raise forms.ValidationError("Please choose a school for director")
        return school
        
    def clean_subjects(self):
        status = self.cleaned_data.get("status") if "status" in self.changed_data else self.instance.status
        subjects = self.cleaned_data.get("subjects")
        if status in [0, 1, 3] and subjects:
            raise forms.ValidationError("This should be completed for inspectors only")
        if status == 2 and not subjects:
            raise forms.ValidationError("Please choose a subject for inspector")
        return subjects

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ExtendedUserChangeFormAdmin, self).save(commit=False)
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        user.is_admin = user.status == 3
        if commit:
            user.save()
        for item in self.cleaned_data["subjects"]:
            user.subjects.add(item)
        if commit:
            user.save()
        return user
