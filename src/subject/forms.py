from django import forms

from models import SubjectPost
from models import Subject


class SubjectPostCreationForm(forms.ModelForm):
    text = forms.Textarea

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SubjectPostCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SubjectPost
        fields = ('name', 'text', 'subject')

    def save(self, commit=True):
        post = super(SubjectPostCreationForm, self).save(commit=False)
        post.author = self.user
        if commit:
            post.save()
        return post


class SubjectPostChangeForm(forms.ModelForm):
    class Meta:
        model = SubjectPost
        fields = ('name', 'text')
        fieldsets = (
          (None, {'fields': (('name', 'subject'), 'text')}),
        )