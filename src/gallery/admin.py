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
from django.contrib.admin.filters import DateFieldListFilter

from gallery.forms import GalleryChangeFormAdmin, GalleryCreationFormAdmin
from utility.admin import AdminChangeMixin, register_model_admin

from .models import Gallery


class GalleryAdmin(AdminChangeMixin):
    icon = '<i class="material-icons">photo</i>'
    change_own_field = "author__id"
    change_own_owner_field = "id"
    
    add_form = GalleryCreationFormAdmin
    change_form = GalleryChangeFormAdmin
    
    add_form_template = "admin/gallery_form.html"
    change_form_template = "admin/gallery_form.html"
    
    list_display = ('name', 'author', 'date', 'my_url_link',)
    list_filter = (
        ('date', DateFieldListFilter),
    )
    readonly_fields = ['author']
    
    search_fields = ('name', 'author__first_name', 'author__last_name', 'date',)

    ordering = ['date']
    
    change_fieldsets = (
        ('Gallery', {'fields': ('name', 'file')}),
        ('Gallery Photos', {'fields': ('gallery_photos', 'gallery_photos_urls', 'id')}),
    )
    
    add_fieldsets = (
        ('Gallery', {'fields': ('name', 'file')}),
        ('Gallery Photos', {'fields': ()}),
    )

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
            return form
    
    pass

register_model_admin(Gallery, GalleryAdmin)
