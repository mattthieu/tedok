from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^manifesti/up_value/(?P<value_id>\d+)/$',
        views.up_value, name='up_value'),
    url(r'^manifesti/down_value/(?P<value_id>\d+)/$',
        views.down_value, name='down_value'),
    url(r'^manifesti$', views.show_manifesti, name='manifesti'),
    url(r'^ressources$', views.show_ressources, name='ressources'),
    url(r'^logbook$', views.show_logbook, name='logbook'),
    url(r'^propositions$', views.show_propositions, name='propositions'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.logout_user, name='logout'),
]
