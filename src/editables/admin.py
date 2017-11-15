from django.contrib import admin

from editables.models import Editable
from utility.admin import register_model_admin


class EditableAdmin(admin.ModelAdmin):

    icon = '<i class="material-icons">content_cut</i>'
    list_display = ['editable_type']

    def my_url_link(self, obj):
        return '<a href="%s">%s</a>' % (
            obj.url_link, 'Access')

    my_url_link.allow_tags = True
    my_url_link.short_description = 'Link to page'


register_model_admin(Editable, EditableAdmin)
