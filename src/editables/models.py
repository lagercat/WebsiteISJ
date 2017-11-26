from django.db import models

from utility.models import CustomPermissionsMixin


class Editable(CustomPermissionsMixin):

    editable_choices = (
        ("1", "Link video"),
        ("2", "Despre noi"),
        ("3", "Banner \"Bine ati venit\""),
        ("4", "Banner Misiune"),
    )

    text = models.TextField(max_length=5000)
    editable_type = models.CharField(
        max_length=3,
        choices=editable_choices,
        unique=True
    )

    class Meta(CustomPermissionsMixin.Meta):
        abstract = False
        verbose_name = 'Editable'
        verbose_name_plural = 'Editables'
        index_text = "Manage"
