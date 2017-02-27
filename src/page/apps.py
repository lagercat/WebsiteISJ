from __future__ import unicode_literals

from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class PageConfig(ModuleMixin, AppConfig):
    name = 'page'
    label = "page"

    verbose_name = "Pages"
    icon = '<i class="material-icons">assignment</i>'

