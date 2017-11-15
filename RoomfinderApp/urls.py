from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^test', views.test, name='test'),
    url(r'^results', views.results, name="results"),
    url(r'^$', views.index, name='index'),
]