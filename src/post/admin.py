from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from models import Post
import os
from django.contrib.admin.widgets import AdminURLFieldWidget
from django.utils.safestring import mark_safe
from django.forms.fields import URLField
    

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
        if commit:
            uploaded_file.save()
        return uploaded_file


class PostChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
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

class URLFieldWidget(AdminURLFieldWidget):
    def render(self, name, value, attrs=None):
        widget = super(URLFieldWidget, self).render(name, value, attrs)
        return mark_safe(u'%s&nbsp;&nbsp;<input type="button" '
                         u'value="View Link" onclick="window.'
                         u'open(document.getElementById(\'%s\')'
                         u'.value)" />' % (widget, attrs['id']))


class PostAdmin(admin.ModelAdmin):
    form = PostChangeForm
    add_form = PostCreationForm
    
    icon = '<i class="material-icons">file</i>'

    list_display = ('name', 'author', 'fileLink', 'date', 'slug',)
    readonly_fields = ['fileLink']
    fieldsets = (
        ('File', {'fields': ('name', 'file')}),
    )
    
    formfield_overrides = {
        URLField: {'widget': URLFieldWidget},
    }
    
    add_fieldsets = (
        ('File', {'fields': ('name', 'file')}),
    )
    
    search_fields = ('author', 'name', 'file', 'date', 'slug',)

    ordering = ['date']
    filter_horizontal = ()
      
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            form = PostCreationForm
            form.current_user = request.user
            return form
        else:
            return super(PostAdmin, self).get_form(request, **kwargs)
    
admin.site.register(Post, PostAdmin)