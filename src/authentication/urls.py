from django.conf.urls import url
from . import views
from django.views import generic

urlpatterns = [
  url('^$', generic.RedirectView.as_view(url='./customers/', permanent=False), name="index"),
  url(r'^logout/$', views.logout_view, name='logout'),
  url(r'^login/', views.login_view, name='login'),
  url(r'^reset/', views.reset_password_view, name="reset")
]
