from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=30)
    message = models.CharField(max_length=2000, null=True)

