# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from post.models import File
from tinymce.models import HTMLField


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
        ('1', 'Primar'),
        ('2', 'Prescolar'),
    )
    type_registration = models.CharField(
        max_length=2,
        choices=school_choices,
    )

    text = HTMLField()
    file = models.FileField(upload_to=user_directory_path, null=True,
                            blank=True)
    REQUIRED = ['name', 'text', 'type_registration']

    def __unicode__(self):
        return self.name

    class Meta(File.Meta):
        abstract = False
        verbose_name = "Enrollment in education"
        verbose_name_plural = "Enrollment in education"
        index_text = "Manage"

    @property
    def url_link(self):
        return "/media/{0}".format(self.file)


@receiver(pre_delete, sender=Registration)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
