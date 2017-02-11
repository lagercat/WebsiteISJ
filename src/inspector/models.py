from __future__ import unicode_literals

from django.db import models
from authentication.models import ExtendedUser

from subject.models import Subject


class Inspector(models.Model):
    user = models.OneToOneField(ExtendedUser)
    subject_one = models.ForeignKey(Subject, related_name='primers', blank=False, null=True, default=-1,
                                    on_delete=models.PROTECT)
    subject_two = models.ForeignKey(Subject, related_name='seconds', blank=True, null=True, default=-1,
                                    on_delete=models.PROTECT)

    def __unicode__(self):
        return self.user.username + " Inspector"
      
    class Meta():
        index_text = "Manage Inspectors"
