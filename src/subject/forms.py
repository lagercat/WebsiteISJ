from django import forms
from models import SubjectPost


class SubjectPostCreationForm(forms.ModelForm):
    class Meta:
        model = SubjectPost
        fields = ('name', 'text', 'subject')

    def save(self, commit=True):
        post = super(SubjectPostCreationForm, self).save(commit=False)
        post.author = self.current_user
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