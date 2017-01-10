from django import forms
from django.contrib import admin

from models import Post
import os
from django.forms.fields import URLField
from view_permission.admin import AdminViewMixin

from post.forms import PostChangeFormAdmin, PostCreationFormAdmin,\
  PageCreationFormAdmin, PageChangeFormAdmin
from post.models import Page

class PostAdmin(AdminViewMixin):
    change_form = PostChangeFormAdmin
    add_form = PostCreationFormAdmin
    
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
  
class PageAdmin(AdminViewMixin):
    change_form = PageChangeFormAdmin
    add_form = PageCreationFormAdmin
    
    icon = '<i class="material-icons">description</i>'

    list_display = ('name', 'author', 'fileLink', 'date', 'slug',)
    readonly_fields = ['fileLink', 'author']

    fieldsets = ()
    change_fieldsets = (
        ('File', {'fields': ('name', 'author', 'text', 'file')}),
    )
    
    add_fieldsets = (
        ('File', {'fields': ('name', 'text', 'file')}),
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
    
admin.site.register(Page, PageAdmin)
admin.site.register(Post, PostAdmin)