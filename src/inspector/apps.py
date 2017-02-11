from __future__ import unicode_literals

from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class InspectorConfig(ModuleMixin, AppConfig):
    name = 'inspector'
    label = "inspector"

    verbose_name = "Inspectors"
    icon = '<i class="material-icons">supervisor_account</i>'