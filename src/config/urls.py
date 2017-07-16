from django.conf.urls import include, url
from django.contrib import admin

from authentication.views import admin_logout_view

urlpatterns = [
    url(r'^search/', include('haystack.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/logout', admin_logout_view, name="admin_logout"),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('homepages.urls')),
    url(r'^', include('authentication.urls')),
    url(r'^', include('post.urls')),
    url(r'^', include('news.urls')),
    url(r'^', include('subject.urls')),
    url(r'^', include('event.urls')),
    url(r'^', include('gallery.urls')),
    url(r'^', include('contact.urls')),
    url(r'^', include('school.urls')),
    url(r'^', include('page.urls')),
]
