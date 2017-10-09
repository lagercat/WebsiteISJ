# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.db import models

from post.models import File


def user_directory_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/registration/{0}{1}'.format(instance.slug,
                                                    file_extension)


# Create your models here.
class Registration(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "registration"
        self._meta.get_field('file').label = "Thumbnail"
        super(Registration, self).__init__(*args, **kwargs)

    school_choices = (
        ('1','Primar'),
        ('2','Prescolar'),
    )
    type_registration = models.CharField(
        max_length=2,
        choices=school_choices,
    )
    REQUIRED = ['name', 'file']

    def __unicode__(self):
        return self.name

    class Meta(File.Meta):
        abstract = False
        verbose_name = "Registration EDU"
        verbose_name_plural = "Registrations EDU"
        index_text = "Manage"


@receiver(pre_delete, sender=Registration)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
