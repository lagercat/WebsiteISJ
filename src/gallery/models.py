from __future__ import unicode_literals
from utility.models import CustomPermissionsMixin
from django.core.urlresolvers import reverse

from django.db import models
import os
from post.models import File
from django.db.models.fields.related import ForeignKey
from django.db.models.fields import IntegerField
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete



class Gallery(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "gallery/thumbnails"
        super(Gallery, self).__init__(*args, **kwargs)

    REQUIRED = ['name', 'file']

    class Meta(File.Meta):
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"
        index_text = "Manage"

class GalleryPhoto(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "gallery/placeholder"
        super(GalleryPhoto, self).__init__(*args, **kwargs)

    gallery = ForeignKey(Gallery, null=False, blank=False, on_delete=models.CASCADE)

    REQUIRED = ['gallery', 'name', 'file']

    def __unicode__(self):
        return self.name

    class Meta(File.Meta):
        abstract = False
        verbose_name = "Gallery Photo"
        verbose_name_plural = "Gallery Photos"
        index_text = "Manage"

@receiver(pre_delete, sender=Gallery)
@receiver(pre_delete, sender=GalleryPhoto)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
