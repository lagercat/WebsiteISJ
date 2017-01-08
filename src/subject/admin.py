from django.contrib import admin

from models import Subject
from models import SubjectPost
from forms import SubjectPostChangeForm, SubjectPostCreationForm
from view_permission.admin import AdminViewMixin


class SubjectAdmin(AdminViewMixin):
    list_display = ['name']
    ordering = ['name']
    icon = '<i class="material-icons">list</i>'
    
class SubjectPostAdmin(AdminViewMixin):
    change_form = SubjectPostChangeForm
    add_form = SubjectPostCreationForm
    list_display = ['name', 'subject', 'author', 'date']
    ordering = ['name', 'subject', 'author', 'date']
    
    icon = '<i class="material-icons">description</i>'
    
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
            form = self.add_form
            form.current_user = request.user
            return form
        else:
            self.fieldsets = self.change_fieldsets
            return self.change_form

admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectPost, SubjectPostAdmin)
