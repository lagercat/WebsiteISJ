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

from event.forms import EventChangeFormAdmin, EventCreationFormAdmin
from models import Event
from utility.admin import AdminChangeMixin, register_model_admin


class EventAdmin(AdminChangeMixin):
    add_form = EventCreationFormAdmin
    change_form = EventChangeFormAdmin
    change_own_field = "author__id"
    change_own_owner_field = "id"

    icon = '<i class="material-icons">room</i>'

    list_display = ('name', 'author', 'address', 'date', 'my_url_link',)
    list_filter = (
        ('date', DateFieldListFilter),
    )
    readonly_fields = ['author']

    search_fields = (
    'name', 'author__first_name', 'author__last_name', 'address', 'date',)

    ordering = ['date']
    filter_horizontal = ()

    change_fieldsets = (
        ('Event Info', {'fields': ('name', 'author')}),
        ('Event Description', {'fields': ('text', 'file')}),
        ('Location and Time', {'fields': ('date', 'address', 'geolocation')}),
    )

    add_fieldsets = (
        ('Event Info', {'fields': ('name',)}),
        ('Event Description', {'fields': ('text', 'file')}),
        ('Location and Time', {'fields': ('date', 'address', 'geolocation')}),
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
            form.text_initial = obj.text
            form.date_initial = obj.date
            form.address_initial = obj.address
            form.geolocation_initial = obj.geolocation
            return form

    pass


register_model_admin(Event, EventAdmin)
