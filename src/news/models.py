from __future__ import unicode_literals

import os

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from post.models import File
from tinymce.models import HTMLField


def user_directory_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/news/{0}{1}'.format(instance.slug, file_extension)


class News(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "thumbnails/news"
        self._meta.get_field('file').label = "Thumbnail"
        super(News, self).__init__(*args, **kwargs)

    text = HTMLField()

    REQUIRED = ['name', 'text', 'file', 'date']

    def __unicode__(self):
        return self.name

    class Meta(File.Meta):
        abstract = False
        verbose_name = "News"
        verbose_name_plural = "News"
        index_text = "Manage"


@receiver(pre_delete, sender=News)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
