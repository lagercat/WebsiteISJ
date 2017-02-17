from django.contrib import admin
from models import Category, Subcategory


# Register your models here.

class PageAdmin(admin.ModelAdmin):
    list_display = ['title']


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Category, PageAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
