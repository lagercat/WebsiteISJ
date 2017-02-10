from __future__ import unicode_literals
import os

from django.db import models
from post.models import File
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from tinymce.models import HTMLField


def user_directory_path(self, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/{0}/{1}{2}'.format(self.slug, file_extension,
                                           self.files_folder())


class Subject(models.Model):
    class Meta:
        verbose_name = "subject"
        verbose_name_plural = "subjects"

    name = models.CharField(max_length=50, null=True, unique=True)

    def __unicode__(self):
        return self.name


class SubjectPost(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "thumbnails/subjectpage"
        super(SubjectPost, self).__init__(*args, **kwargs)

    text = HTMLField()
    subject = models.ForeignKey(Subject, blank=False, null=False)

    REQUIRED = ['subject', 'name', 'text', 'file']

    def __unicode__(self):
        return self.name

    class Meta(File.Meta):
        verbose_name = "post"
        verbose_name_plural = "posts"

    
@receiver(pre_delete, sender=SubjectPost)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)