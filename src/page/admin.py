# Copyright 2017 Adrian-Ioan Garovat, Emanuel Covaci, Sebastian-Valeriu Males
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
from django.contrib import admin
from django.contrib.admin.filters import DateFieldListFilter

from forms import (ArticleChangeFormAdmin, ArticleCreationFormAdmin,
                   SimplePageChangeFormAdmin, SimplePageCreationFormAdmin,
                   CategoryChangeFormAdmin, CategoryCreationFormAdmin)
from utility.admin import AdminChangeMixin, register_model_admin

from .models import Article, Category, SimplePage, Subcategory


class ArticleAdmin(AdminChangeMixin):
    change_form = ArticleChangeFormAdmin
    add_form = ArticleCreationFormAdmin
    change_own_field = "author__id"
    change_own_owner_field = "id"

    icon = '<i class="material-icons">assignment</i>'
    list_display = ['short_name', 'subcategory', 'author', 'date',
                    'my_url_link']
    list_filter = (
        ('date', DateFieldListFilter),
    )
    readonly_fields = ['author']

    fieldsets = ()
    change_fieldsets = (
        ('Page', {'fields': ('name', 'subcategory', 'author')}),
        ('Article content', {'fields': ('text', 'file')})
    )

    add_fieldsets = (
        ('Page', {'fields': ('name', 'subcategory')}),
        ('Article content', {'fields': ('text', 'file')})
    )

    search_fields = (
        'author__first_name', 'author__last_name', 'name', 'date', 'slug',)

    ordering = ['-date']
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
            form.text_initial = obj.text
            return form

    pass


class SimplePageAdmin(AdminChangeMixin):
    change_form = SimplePageChangeFormAdmin
    add_form = SimplePageCreationFormAdmin
    change_own_field = "author__id"
    change_own_owner_field = "id"

    icon = '<i class="material-icons">list</i>'
    list_display = ['short_name', 'category', 'author', 'date',
                    'my_url_link']
    list_filter = (
        ('date', DateFieldListFilter),
    )
    readonly_fields = ['author']

    fieldsets = ()
    change_fieldsets = (
        ('Page', {'fields': ('name', 'category', 'author')}),
        ('Simple plage content', {'fields': ('text', 'file')})
    )

    add_fieldsets = (
        ('Page', {'fields': ('name', 'category')}),
        ('Simple page content', {'fields': ('text', 'file')})
    )

    search_fields = (
        'author__first_name', 'author__last_name', 'name', 'date', 'slug',)

    ordering = ['-date']
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
            form.text_initial = obj.text
            return form

    pass


class PageAdmin(admin.ModelAdmin):
    change_form = CategoryChangeFormAdmin
    add_form = CategoryCreationFormAdmin

    icon = '<i class="material-icons">chrome_reader_mode</i>'
    list_display = ['title', 'my_url_link']

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            form = self.add_form
            form.current_user = request.user
            return form
        else:
            form = self.change_form
            form.order_initial = obj.order
            return form

    def my_url_link(self, obj):
        return '<a href="%s">%s</a>' % (
            obj.url_link, 'Access')

    my_url_link.allow_tags = True
    my_url_link.short_description = 'Link to page'


class SubcategoryAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">dashboard</i>'
    list_display = ['name', 'my_url_link']

    def my_url_link(self, obj):
        return '<a href="%s">%s</a>' % (
            obj.url_link, 'Access')

    my_url_link.allow_tags = True
    my_url_link.short_description = 'Link to page'


register_model_admin(Category, PageAdmin)
register_model_admin(Subcategory, SubcategoryAdmin)

register_model_admin(Article, ArticleAdmin)
register_model_admin(SimplePage, SimplePageAdmin)
