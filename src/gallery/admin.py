from django.contrib import admin
from .models import Gallery

from view_permission.admin import AdminViewMixin


# Register your models here.

class GalleryAdmin(AdminViewMixin):
    list_display = ['name']
    ordering = ['name']


admin.site.register(Gallery, GalleryAdmin)
