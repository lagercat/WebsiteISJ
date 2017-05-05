from __future__ import unicode_literals

from django.db import models

from material.frontend.models import Module


# Create your models here.


class CustomPermissionsMixin(models.Model):
    """
        Mixin adds view permission to model.
    """
    class Meta:
        abstract = True
        default_permissions = ('change', 'view', 'change_own', 'delete', 'add_own')
        
def make_view_proxy(model):
    class Meta(model.Meta):
        app_label = model._meta.app_label
        verbose_name = model._meta.verbose_name
        verbose_name_plural = model._meta.verbose_name_plural
        proxy = True
        index_text = "View all"
    
    attrs = {'__module__': "", 'Meta': Meta, "__name__": model.__name__}
    cls = type(str(model.__name__ + "Proxy"), (model,), attrs)
    return cls
          
class ModuleProxy(Module, CustomPermissionsMixin):
    class Meta(CustomPermissionsMixin.Meta):
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        app_label = Module._meta.app_label
        abstract = False
        proxy = True
        index_text = "View all"
        
    __name__ = Module.__name__
