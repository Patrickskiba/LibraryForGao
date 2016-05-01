from django.conf.urls import url

from . import views

app_name = 'books'

urlpatterns = [
    url(r'^$', views.browse, name='browse'),
    url(r'^rent/(?P<id>[0-9]+)/$', views.rent, name='rent'),
    url(r'^(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^results/$', views.search_titles, name='search_titles'),
]