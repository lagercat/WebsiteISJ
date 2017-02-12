from __future__ import unicode_literals

from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class GalleryConfig(ModuleMixin, AppConfig):
    name = 'gallery'
    label = "gallery"

    verbose_name = "Galleries"
    icon = '<i class="material-icons">photo</i>'

