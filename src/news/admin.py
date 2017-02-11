from django.contrib import admin

from .models import News
from view_permission.admin import AdminViewMixin


class NewsAdmin(AdminViewMixin):
    list_display = ['title']
    ordering = ['title']
    icon = '<i class="material-icons">rss_feed</i>'


admin.site.register(News, NewsAdmin)
