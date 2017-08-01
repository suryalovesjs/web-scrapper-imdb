from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main,name='mainindex'),
    url(r'^popular/$', views.popular,name='popular'),
    url(r'^genre/(?P<genre_name>[a-z]+)$', views.genre,name='genre'),
]
