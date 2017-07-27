from __future__ import unicode_literals

from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'news'
    label = "news"

    verbose_name = "News"
    icon = '<i class="material-icons">rss_feed</i>'
