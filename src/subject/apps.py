from __future__ import unicode_literals

from django.apps import AppConfig

from material.frontend.apps import ModuleMixin


class SubjectConfig(ModuleMixin, AppConfig):
    name = 'subject'
    label = "subject"

    verbose_name = "Subjects"
    icon = '<i class="material-icons">list</i>'
