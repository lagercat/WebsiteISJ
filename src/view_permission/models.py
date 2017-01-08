from __future__ import unicode_literals

from django.db import models

# Create your models here.

class CustomPermissionsMixin(models.Model):
    """
        Mixin adds view permission to model.
    """
    class Meta:
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'view', 'change_own')