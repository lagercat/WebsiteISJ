from django import forms

from models import Post


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['file']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreatePostForm, self).__init__(*args, **kwargs)