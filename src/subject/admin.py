# Copyright 2017 Adrian-Ioan Gărovăț, Emanuel Covaci, Sebastian-Valeriu Maleș
#
# This file is part of WebsiteISJ
#
# WebsiteISJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebsiteISJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
from django.contrib.admin.filters import DateFieldListFilter

from forms import (SubcategoryChangeFormAdmin, SubcategoryCreationFormAdmin,
                   SubjectPostChangeFormAdmin, SubjectPostCreationFormAdmin)
from models import Subcategory, Subject, SubjectPost
from utility.admin import AdminChangeMixin, register_model_admin


class SubjectAdmin(AdminChangeMixin):
    list_display = ['name', 'my_url_link']
    ordering = ['name']
    icon = '<i class="material-icons">import_contacts</i>'

    def my_url_link(self, obj):
        return '<a href="%s">%s</a>' % (
            obj.url_link, 'Access')

    my_url_link.allow_tags = True
    my_url_link.short_description = 'Link to page'


class SubcategoryAdmin(AdminChangeMixin):
    change_form = SubcategoryChangeFormAdmin
    add_form = SubcategoryCreationFormAdmin
    change_own_field = "subject__in"
    change_own_owner_field = "subjects"

    icon = '<i class="material-icons">queue</i>'

    list_display = ('name', 'author', 'subject', 'date', 'my_url_link',)
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
        ('Page', {'fields': ('name', 'subject',)}),
        ('Page content', {'fields': ('file',)})
    )

    search_fields = (
        'author__first_name', 'author__last_name', 'name', 'date', 'slug', 'subject')

    ordering = ['date']
    filter_horizontal = ()

    def my_url_link(self, obj):
        return '<a href="%s">%s</a>' % (
            obj.url_link, 'Access')

    my_url_link.allow_tags = True
    my_url_link.short_description = 'Link to page'

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
    change_own_field = "subject__in"
    change_own_owner_field = "subjects"
    list_display = ['name', 'subject', 'subcategory', 'author',
                    'date', 'my_url_link']
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

    def my_url_link(self, obj):
        return '<a href="%s">%s</a>' % (
            obj.url_link, 'Access')

    my_url_link.allow_tags = True
    my_url_link.short_description = 'Link to page'

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
