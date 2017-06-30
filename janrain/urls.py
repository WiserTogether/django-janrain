from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='janrain_login'),
    url(r'^logout/$', views.logout, name='janrain_logout'),
]
