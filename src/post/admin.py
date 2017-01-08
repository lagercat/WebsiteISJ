from django import forms
from django.contrib import admin

from models import Post
import os
from django.forms.fields import URLField
from view_permission.admin import AdminViewMixin
    

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'file',)

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        max_size = 10000000  # 10 MB
        filename, file_type = os.path.splitext(uploaded_file.name)
        allowed_file_types = [
            '.doc', '.docx', '.docm', '.xls', '.xlsx', '.ppt',
            '.ppt', '.pps', '.zip', '.rar', '.jpg', '.jpeg'
            '.png', '.gif', '.bmp', '.txt', '.tif', '.rtf', '.pdf',
            '.odt', '.ace', '.ods', '.odg'
        ]
        if not(any(file_type in type for type in allowed_file_types)):
            raise forms.ValidationError("Fisierul nu se incadreaza in extensile permise")
        if uploaded_file.size > max_size:
            raise forms.ValidationError("Fisierul trece de dimensiunea maxima de %d" % max_size)

        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(PostCreationForm, self).save(commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.author_status = self.current_user.status
        if commit:
            uploaded_file.save()
        return uploaded_file


class PostChangeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'file')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        max_size = 10000000  # 10 MB
        filename, file_type = os.path.splitext(uploaded_file.name)
        allowed_file_types = [
            '.doc', '.docx', '.docm', '.xls', '.xlsx', '.ppt',
            '.ppt', '.pps', '.zip', '.rar', '.jpg', '.jpeg'
            '.png', '.gif', '.bmp', '.txt', '.tif', '.rtf', '.pdf',
            '.odt', '.ace', '.ods', '.odg'
        ]
        if not(any(file_type in type for type in allowed_file_types)):
            raise forms.ValidationError("Fisierul nu se incadreaza in extensile permise")
        if uploaded_file.size > max_size:
            raise forms.ValidationError("Fisierul trece de dimensiunea maxima de %d" % max_size)

        return uploaded_file


class PostAdmin(AdminViewMixin):
    change_form = PostChangeForm
    add_form = PostCreationForm
    
    icon = '<i class="material-icons">description</i>'

    list_display = ('name', 'author', 'fileLink', 'date', 'slug',)
    readonly_fields = ['fileLink', 'author']

    fieldsets = ()
    change_fieldsets = (
        ('File', {'fields': ('name', 'author', 'file')}),
    )
    
    add_fieldsets = (
        ('File', {'fields': ('name', 'file')}),
    )
    
    search_fields = ('author__first_name', 'author__last_name', 'name', 'date', 'slug',)

    ordering = ['date']
    filter_horizontal = ()
      
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fieldsets = self.add_fieldsets
            form = self.add_form
            form.current_user = request.user
            return form
        else:
            self.fieldsets = self.change_fieldsets
            return self.change_form
    
    pass
    
admin.site.register(Post, PostAdmin)