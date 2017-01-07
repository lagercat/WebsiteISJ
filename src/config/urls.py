from django.conf.urls import url, include
from django.contrib import admin

from material.frontend import urls as frontend_urls

urlpatterns = [
  url(r'', include(frontend_urls)),
  url(r'^admin/', admin.site.urls),
  url(r'^', include('homepages.urls')),
  url(r'^', include('authentication.urls')),
  url(r'^', include('post.urls'))
]