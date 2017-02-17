from django.contrib import admin
from models import Header_tile, Subcategory_heder_tile


# Register your models here.

class PageAdmin(admin.ModelAdmin):
    list_display = ['title']


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Header_tile, PageAdmin)
admin.site.register(Subcategory_heder_tile, SubcategoryAdmin)
