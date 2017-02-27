from __future__ import unicode_literals

from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class ContactConfig(ModuleMixin, AppConfig):
    name = 'contact'
    label = "contact"
    verbose_name = "Contacts"
    icon = '<i class="material-icons">contact_mail</i>'
