from __future__ import unicode_literals

from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class EventConfig(ModuleMixin, AppConfig):
    name = 'event'
    label = "event"

    verbose_name = "Events"
    icon = '<i class="material-icons">room</i>'
