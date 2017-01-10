from __future__ import unicode_literals

from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class PostConfig(ModuleMixin, AppConfig):
    name = 'post'
    icon = '<i class="material-icons">description</i>'
