from django.conf.urls import url, include
from django.contrib import admin

from material.frontend import urls as frontend_urls
from authentication.views import admin_logout_view

urlpatterns = [
  url(r'^tinymce/', include('tinymce.urls')),
  url(r'^admin/logout', admin_logout_view, name="admin_logout"),
  url(r'^admin/', admin.site.urls),
  url(r'^', include('homepages.urls')),
  url(r'^', include('authentication.urls')),
  url(r'^', include('post.urls')),
  url(r'^', include('news.urls')),
  url(r'^', include('subject.urls')),
  url(r'^', include('event.urls'))
]