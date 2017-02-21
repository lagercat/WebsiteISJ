from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=30)
    subject = models.CharField(max_length=50)
    message = models.TextField()

    def __unicode__(self):
        return self.email

    class Meta():
        get_latest_by = 'first_name'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        index_text = "Manage"

