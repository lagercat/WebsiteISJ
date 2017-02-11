from __future__ import unicode_literals

from django.apps import AppConfig
from material.frontend.apps import ModuleMixin

class AuthenticationConfig(ModuleMixin, AppConfig):
    name = 'authentication'
    label = "authentication"

    verbose_name = "Users"
    icon = '<i class="material-icons">people</i>'
