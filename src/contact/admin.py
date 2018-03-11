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
from django.contrib import admin

from utility.admin import AdminChangeMixin

from contact.models import Contact


class ContactAdmin(AdminChangeMixin):
    can_change_own = False
    add_form = Contact
    icon = '<i class="material-icons">contact_mail</i>'
    readonly_fields = ('date',)
    fields = ('first_name', 'last_name', 'date', 'email', 'subject', 'message')
    list_display = ['first_name', 'last_name', 'email', 'subject', 'date']


admin.site.register(Contact, ContactAdmin)
