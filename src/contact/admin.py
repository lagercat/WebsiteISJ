from django.contrib import admin

from utility.admin import AdminChangeMixin

from .models import Contact


class ContactAdmin(AdminChangeMixin):
    can_change_own = False
    add_form = Contact
    icon = '<i class="material-icons">contact_mail</i>'
    list_display = ['first_name', 'last_name', 'email', 'subject']

admin.site.register(Contact, ContactAdmin)
