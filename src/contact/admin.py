

# Register your models here.
from django.contrib import admin
from .models import Contact
from utility.admin import AdminChangeMixin

class ContactAdmin(AdminChangeMixin):
    add_form = Contact
    icon = '<i class="material-icons">contact_mail</i>'
    list_display = ['first_name', 'last_name', 'email','subject']

admin.site.register(Contact,ContactAdmin)
