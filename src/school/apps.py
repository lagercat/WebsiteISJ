from __future__ import unicode_literals

from django.apps import AppConfig

from material.frontend.apps import ModuleMixin


class SchoolConfig(ModuleMixin, AppConfig):
    name = 'school'
    label = "school"

    verbose_name = "Schools"
    icon = '<i class="material-icons">location_city</i>'
