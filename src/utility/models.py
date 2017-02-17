from __future__ import unicode_literals

from django.db import models

# Create your models here.

class CustomPermissionsMixin(models.Model):
    """
        Mixin adds view permission to model.
    """
    class Meta:
        abstract = True
        default_permissions = ('change', 'view', 'change_own')
        
def make_view_proxy(model):
    class Meta(model.Meta):
        app_label = model._meta.app_label
        proxy = True
        index_text = "View all"
        
    attrs = {'__module__': "", 'Meta': Meta, "__name__": model.__name__}
    cls = type(str(model.__name__ + "Proxy"), (model,), attrs)
    
    return cls
          
  
