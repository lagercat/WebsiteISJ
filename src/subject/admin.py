from django.contrib import admin

from models import Subject
from models import SubjectPost, Subcategory
from forms import SubjectPostChangeFormAdmin, SubjectPostCreationFormAdmin,SubcategoryCreationFormAdmin,SubcategoryChangeFormAdmin

from utility.admin import AdminChangeMixin, register_model_admin
from django.contrib.admin.filters import DateFieldListFilter, ChoicesFieldListFilter


class SubjectAdmin(AdminChangeMixin):
    list_display = ['name']
    ordering = ['name']
    icon = '<i class="material-icons">import_contacts</i>'


class SubcategoryAdmin(AdminChangeMixin):
    change_form = SubcategoryChangeFormAdmin
    add_form = SubcategoryCreationFormAdmin
    change_own_field = "author__id"
    change_own_owner_field = "id"

    icon = '<i class="material-icons">queue</i>'

    list_display = ('name', 'author', 'subject', 'date', 'slug',)
    list_filter = (
        ('date', DateFieldListFilter),
        'subject'
    )
    readonly_fields = ['fileLink', 'author']

    fieldsets = ()
    change_fieldsets = (
        ('Page', {'fields': ('name', 'author')}),
        ('Page content', {'fields': ('subject', 'file',)})
    )

    add_fieldsets = (
        ('Page', {'fields': ('name','subject',)}),
        ('Page content', {'fields': ('file',)})
    )

    search_fields = (
    'author__first_name', 'author__last_name', 'name', 'date', 'slug', 'subject')

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
            form = self.change_form
            form.current_user = request.user
            return form

    pass




class SubjectPostAdmin(AdminChangeMixin):
    change_form = SubjectPostChangeFormAdmin
    add_form = SubjectPostCreationFormAdmin
    change_own_field = "author__id"
    change_own_owner_field = "id"
    list_display = ['name', 'subject', 'subcategory', 'author',
                    'date', 'slug']
    list_filter = (
        ('date', DateFieldListFilter),
        'subject'
    )
    change_readonly_fields = ['author']
    add_readonly_fields = []

    ordering = ['name', 'subcategory', 'subject', 'author', 'date']

    icon = '<i class="material-icons">description</i>'

    fieldsets = ()

    change_fieldsets = (
        ('Page', {'fields': ('name', ('subcategory', 'subject'), 'author')}),
        ('Page content', {'fields': ('text', 'file')})
    )

    add_fieldsets = (
        ('Page', {'fields': ('name', ('subcategory', 'subject'),)}),
        ('Page content', {'fields': ('text', 'file')})
    )

    search_fields = (
        'author__first_name', 'author__last_name', 'name', 'subcategory',
        'subject', 'author',
        'date')

    ordering = ['date']
    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.fieldsets = self.add_fieldsets
            self.readonly_fields = self.add_readonly_fields
            form = self.add_form
            form.current_user = request.user
            return form
        else:
            self.fieldsets = self.change_fieldsets
            self.readonly_fields = self.change_readonly_fields
            form = self.change_form
            form.current_user = request.user
            form.text_initial = obj.text
            return form


register_model_admin(Subject, SubjectAdmin)
register_model_admin(SubjectPost, SubjectPostAdmin)
register_model_admin(Subcategory, SubcategoryAdmin)
