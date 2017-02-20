from django.contrib import admin

from .models import Article, Category, Subcategory,SimplePage
from utility.admin import AdminChangeMixin
from forms import ArticleCreationFormAdmin, ArticleChangeFormAdmin
from forms import SimplePageChangeFormAdmin,SimplePageCreationFormAdmin
from django.contrib.admin.filters import DateFieldListFilter


class ArticleAdmin(AdminChangeMixin):
    change_form = ArticleChangeFormAdmin
    add_form = ArticleCreationFormAdmin

    icon = '<i class="material-icons">assignment</i>'
    list_display = ['short_name', 'subcategory', 'author', 'fileLink', 'date',
                    'slug']
    list_filter = (
        ('date', DateFieldListFilter),
    )
    readonly_fields = ['fileLink', 'author']

    fieldsets = ()
    change_fieldsets = (
        ('Page', {'fields': ('name', 'subcategory', 'author', 'date')}),
        ('Article content', {'fields': ('text', 'file')})
    )

    add_fieldsets = (
        ('Page', {'fields': ('name', 'subcategory', 'date')}),
        ('Article content', {'fields': ('text', 'file')})
    )

    search_fields = (
        'author__first_name', 'author__last_name', 'name', 'date', 'slug',)

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


class SimplePageAdmin(AdminChangeMixin):
    change_form = SimplePageChangeFormAdmin
    add_form = SimplePageCreationFormAdmin

    icon = '<i class="material-icons">list</i>'
    list_display = ['short_name', 'category', 'author', 'fileLink', 'date',
                    'slug']
    list_filter = (
        ('date', DateFieldListFilter),
    )
    readonly_fields = ['fileLink', 'author']

    fieldsets = ()
    change_fieldsets = (
        ('Page', {'fields': ('name', 'category', 'author', 'date')}),
        ('Simple plage content', {'fields': ('text', 'file')})
    )

    add_fieldsets = (
        ('Page', {'fields': ('name', 'category', 'date')}),
        ('Simple page content', {'fields': ('text', 'file')})
    )

    search_fields = (
        'author__first_name', 'author__last_name', 'name', 'date', 'slug',)

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


class PageAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">chrome_reader_mode</i>'
    list_display = ['title']


class SubcategoryAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">dashboard</i>'
    list_display = ['name']


admin.site.register(Category, PageAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)

admin.site.register(Article, ArticleAdmin)
admin.site.register(SimplePage,SimplePageAdmin)
