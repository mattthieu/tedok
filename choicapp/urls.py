from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^manifesti$', views.show_manifesti, name='manifesti'),
    url(r'^ressources$', views.show_ressources, name='ressources'),
    url(r'^logbook$', views.show_logbook, name='logbook'),
    url(r'^propositions$', views.show_propositions, name='propositions'),
]
