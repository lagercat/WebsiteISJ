from django.contrib import admin
from .models import Gallery

from view_permission.admin import AdminViewMixin
from gallery.forms import GalleryChangeFormAdmin, GalleryCreationFormAdmin
from gallery.models import GalleryPhoto
from gallery.views import gallery


# Register your models here.

class GalleryAdmin(AdminViewMixin):
    list_display = ['name']
    ordering = ['name']
    icon = '<i class="material-icons">photo</i>'
    
    add_form = GalleryCreationFormAdmin
    change_form = GalleryChangeFormAdmin
    
    add_form_template = "admin/gallery_form.html"
    change_form_template = "admin/gallery_form.html"
    
    search_fields = ('name',)
    
    change_fieldsets = (
        ('Gallery', {'fields': ('name', 'file')}),
        ('Gallery Photos', {'fields': ('gallery_photos', 'gallery_photos_urls', 'id')}),
    )
    
    add_fieldsets = (
        ('Gallery', {'fields': ('name', 'file')}),
        ('Gallery Photos', {'fields': ()}),
    )
      
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

admin.site.register(Gallery, GalleryAdmin)