from django import forms
from django.contrib import admin

from models import Post
import os
from django.forms.fields import URLField
from view_permission.admin import AdminViewMixin

from post.forms import PostChangeFormAdmin, PostCreationFormAdmin,\
  PageCreationFormAdmin, PageChangeFormAdmin
from post.models import Page
from django.http.response import HttpResponseRedirect, HttpResponse
from django.conf.urls import url
from post import views

class PostAdmin(AdminViewMixin):
    change_form = PostChangeFormAdmin
    add_form = PostCreationFormAdmin
    
    add_form_template = "admin/add_files_form.html"
    
    icon = '<i class="material-icons">description</i>'

    list_display = ('short_name', 'author', 'fileLink', 'location', 'date', 'slug',)
    readonly_fields = ['fileLink', 'author', 'location']

    fieldsets = ()
    change_fieldsets = (
        ('File', {'fields': ('name', 'author', ('file', 'location'))}),
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
          

class PageAdmin(AdminViewMixin):
    change_form = PageChangeFormAdmin
    add_form = PageCreationFormAdmin
    
    icon = '<i class="material-icons">description</i>'

    list_display = ('short_name', 'author', 'fileLink', 'date', 'slug',)
    readonly_fields = ['fileLink', 'author']

    fieldsets = ()
    change_fieldsets = (
        ('Page', {'fields': ('name', 'author')}),
        ('Page content', {'fields': ('text', 'file')})
    )
    
    add_fieldsets = (
        ('Page', {'fields': ('name',)}),
        ('Page content', {'fields': ('text', 'file')})
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
            form = self.change_form
            form.text_initial = obj.text
            return form
    
    pass
    
admin.site.register(Page, PageAdmin)
admin.site.register(Post, PostAdmin)