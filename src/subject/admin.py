from django import forms
from django.contrib import admin

from models import Subject
from subject.models import SubjectPost


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    
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

    
class SubjectPostAdmin(admin.ModelAdmin):
    form = SubjectPostChangeForm
    add_form = SubjectPostCreationForm
    list_display = ['name', 'subject', 'author', 'date']
    ordering = ['name', 'subject', 'author', 'date']
    
    icon = '<i class="material-icons">file</i>'
    
    fieldsets = ()
    
    change_fieldsets = (
        (None, {'fields': ('name', 'text')}),
    )
    
    add_fieldsets = (
        (None, {'fields': (('name', 'subject'), 'text')}),
    )
    
    search_fields = ('name', 'subject', 'author', 'date')

    ordering = ['date']
    filter_horizontal = ()
      
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fieldsets = self.add_fieldsets
            form = SubjectPostCreationForm
            form.current_user = request.user
            return form
        else:
            self.fieldsets = self.change_fieldsets
            return super(SubjectPostAdmin, self).get_form(request, **kwargs)

admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectPost, SubjectPostAdmin)
