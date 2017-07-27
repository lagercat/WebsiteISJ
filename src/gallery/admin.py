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
    
    list_display = ('name', 'author', 'date', 'slug',)
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
