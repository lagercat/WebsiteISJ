# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-10 21:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import event.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=5000, null=True)),
                ('location', models.CharField(max_length=100, null=True)),
                ('time', models.DateTimeField(null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=event.models.user_directory_path)),
                ('slug', models.SlugField(default=uuid.uuid1, unique=True)),
                ('author', models.ForeignKey(blank='False', on_delete=django.db.models.deletion.CASCADE, related_name='event_post', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view', 'change_own'),
                'abstract': False,
                'get_latest_by': 'time',
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
    ]
