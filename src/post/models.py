from __future__ import unicode_literals
import os
import uuid

from authentication.models import ExtendedUser
from django.db import models
from view_permission.models import CustomPermissionsMixin
from tinymce.models import HTMLField
from django.template.defaultfilters import truncatechars
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


def user_directory_path(self, filename):
    filename, file_extension = os.path.splitext(filename)
    return './documents/{0}/{1}{2}'.format(self.location,
                                           self.slug, file_extension)

class File(CustomPermissionsMixin):

    author = models.ForeignKey(ExtendedUser, blank=False)
    name = models.CharField(max_length=100, blank=False, null=True)
    file = models.FileField(upload_to=user_directory_path)
    date = models.DateTimeField(auto_now_add=True, editable=False, blank=False, null=True)
    slug = models.SlugField(default=uuid.uuid1, unique=True,editable=False)
    location = models.CharField(max_length=50, default="abstract")

    @property
    def filename(self):
        return os.path.basename(self.file.url)

    def fileLink(self):
      if self.file:
          return '<a href="' + str(self.file.url) + '">' + "See file" + '</a>'
      else:
          return '<a href="''"></a>'
    fileLink.allow_tags = True
    fileLink.short_description = "File Link"

    def __unicode__(self):
        return "File %s from %s" % (self.filename, self.author.username)
      
    @property
    def short_name(self):
        return truncatechars(self.name, 40)

    class Meta(CustomPermissionsMixin.Meta):
        abstract = True
        get_latest_by = 'date'
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        
class Post(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "interior"
        super(Post, self).__init__(*args, **kwargs)
      
    REQUIRED = ['name', 'file']
    
    class Meta(File.Meta):
        abstract = False
        get_latest_by = 'date'
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        
class Page(File):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('location').default = "thumbails/pages"
        super(Page, self).__init__(*args, **kwargs)
      
    text = HTMLField()

    REQUIRED = ['name', 'text', 'file']
  
    class Meta(Post.Meta):
        abstract = False
        get_latest_by = 'date'
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

@receiver(pre_delete, sender=Page)       
@receiver(pre_delete, sender=Post)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
        