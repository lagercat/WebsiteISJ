from __future__ import unicode_literals

from django.db import models


class Subject(models.Model):
    class Meta:
      verbose_name = "subject"
      verbose_name_plural = "subjects"
      
    name = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return self.name

class SubjectPost(models.Model):
    class Meta:
      verbose_name = "post"
      verbose_name_plural = "posts"
    
    name = models.CharField(max_length=50, null=True)
    text = models.TextField()  
    subject = models.ForeignKey(Subject, blank=False, null=False)
    author = models.ForeignKey("authentication.ExtendedUser", blank=False, null=False)
    date = models.DateTimeField(editable=False, auto_now_add=True, blank=False, null=True)
    
    REQUIRED = ['subject', 'name', 'text']
    
    def __unicode__(self):
        return self.name
