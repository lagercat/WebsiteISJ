from __future__ import unicode_literals

from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class HeadmasterConfig(ModuleMixin, AppConfig):
    name = 'headmaster'
    label = "headmaster"

    verbose_name = "Headmasters"
    icon = '<i class="material-icons">event_seat</i>'

