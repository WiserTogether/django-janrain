from django.conf.urls import url

urlpatterns = [
    url(r'^login/$', 'login', name='janrain_login'),
    url(r'^logout/$', 'logout', name='janrain_logout'),
]
