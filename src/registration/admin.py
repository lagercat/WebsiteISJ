# -*- coding: utf-8 -*-
from django.contrib.admin.filters import DateFieldListFilter

from .forms import RegistrationChangeFormAdmin
from .forms import RegistrationCreationFormAdmin
from utility.admin import AdminChangeMixin
from utility.admin import register_model_admin

from .models import Registration

class RegistrationAdmin(AdminChangeMixin):
    change_form = RegistrationChangeFormAdmin
    add_form = RegistrationCreationFormAdmin
    change_own_field = "author__id"
    change_own_owner_field = "id"

    icon = '<i class="material-icons">rss_feed</i>'

    list_display = ('short_name', 'author', 'date', 'type_registration',
                    'my_url_link',)
    list_filter = (
        ('date', DateFieldListFilter),
    )
    readonly_fields = ['author']

    fieldsets = ()
    change_fieldsets = (
        ('Page', {'fields': ('name',)}),
        ('Registration content', {'fields': ('type_registration','text', 'file')})
    )

    add_fieldsets = (
        ('Page', {'fields': ('name',)}),
        ('Registration content', {'fields': ('type_registration','text', 'file')})
    )

    search_fields = (
        'author__first_name', 'author__last_name', 'name', 'date',
        'type_registration','text', 'slug',)

    ordering = ['date']
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
            return form

    pass


register_model_admin(Registration, RegistrationAdmin)