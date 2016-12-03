import os

from django import forms

from models import Post


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['file']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreatePostForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        max_size = 10  # We should discuss the maximum file size
        filename, file_type = os.path.splitext(uploaded_file.name)
        allowed_file_types = [
            'doc', 'docx', 'docm', 'xls', 'xlsx', 'ppt',
            'ppt', 'pps', 'zip', 'rar', 'jpg', 'jpg', 'jpeg'
            'png', 'gif', 'bmp', 'txt', 'tif', 'rtf', 'pdf',
            'odt', 'ace', 'ods', 'odg'
        ]
        if file_type not in allowed_file_types:
            raise forms.ValidationError("Fisierul nu se incadreaza in extensile permise")
        if uploaded_file.size > max_size:
            raise forms.ValidationError("Fisierul trece de dimensiunea maxima de %d" % max_size)

        return uploaded_file
