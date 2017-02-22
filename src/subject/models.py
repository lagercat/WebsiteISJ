from __future__ import unicode_literals
import os

from django.db import models
from post.models import File
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from tinymce.models import HTMLField
from utility.models import CustomPermissionsMixin
from bokeh.core.properties import abstract


def user_directory_path(self, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/{0}/{1}{2}'.format(self.slug, file_extension,
                                           self.files_folder())


class Subject(CustomPermissionsMixin):
    class Meta(CustomPermissionsMixin.Meta):
        abstract = False
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        index_text = "Create"

    name = models.CharField(max_length=50, null=True, unique=True)

    def __unicode__(self):
        return self.name


class Subcategory(CustomPermissionsMixin):
    name = models.CharField(max_length=50, null=False, unique=True)
    subject = models.ForeignKey(Subject, blank=False, null=False)

    class Meta(File.Meta):
        abstract = False
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"
        index_text = "Manage"

    def __unicode__(self):
        return self.name


class SubjectPost(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "thumbnails/subjectpage"
        self._meta.get_field('file').label = "Thumbnail"
        super(SubjectPost, self).__init__(*args, **kwargs)

    text = HTMLField()
    subcategory = models.ForeignKey(Subcategory, blank=True, null=True)
    subject = models.ForeignKey(Subject, blank=True, null=True)

    REQUIRED = ['subject','subcategory', 'name', 'text', 'file']

    def __unicode__(self):
        return self.name

    class Meta(File.Meta):
        abstract = False
        verbose_name = "Subject Page"
        verbose_name_plural = "Subject Pages"
        index_text = "Manage"


@receiver(pre_delete, sender=SubjectPost)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
