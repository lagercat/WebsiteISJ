from __future__ import unicode_literals

from django.db import models
from authentication.models import ExtendedUser

from school.models import School


class Headmaster(models.Model):
    user = models.OneToOneField(ExtendedUser)
    school = models.ForeignKey(School, related_name='headmasters', blank=False, null=True, default=-1,
                               on_delete=models.PROTECT)

    def __unicode__(self):
        return self.user.username + " Headmaster"

    class Meta():
        index_text = "Manage Headmasters"