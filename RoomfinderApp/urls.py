from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^building/(?P<building>\w+)$', views.result),
    url(r'^update', views.update, name='update'),
    url(r'^$', views.index, name='index'),
]