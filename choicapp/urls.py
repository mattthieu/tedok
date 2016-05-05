from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^manifesti/up_value/(?P<value_id>\d+)/(?P<nb_votes>\d+)/$',
        views.up_value, name='up_value'),
    url(r'^manifesti/down_value/(?P<value_id>\d+)/(?P<nb_votes>\d+)/$',
        views.down_value, name='down_value'),
    url(r'^manifesti$', views.show_manifesti, name='manifesti'),
    url(r'^add_value/$', views.AddValue.as_view(), name='add_value'),
    url(r'^edit_value/(?P<value_id>\d+)/$',
        views.AddValue.as_view(), name='edit_value'),
    url(r'^add_logbookpost/$',
        views.AddLogBookPost.as_view(), name='add_logbookpost'),
    url(r'^edit_logbookpost/(?P<logbookpost_id>\d+)/$',
        views.AddLogBookPost.as_view(), name='edit_logbookpost'),
    url(r'^add_glossaryword/$',
        views.GlossaryWordCreate.as_view(), name='add_glossaryword'),
    url(r'^edit_glossaryword/(?P<pk>[0-9]+)/$',
        views.GlossaryWordUpdate.as_view(), name='edit_glossaryword'),
    url(r'^ressources$', views.show_ressources, name='ressources'),
    url(r'^glossary$', views.show_glossary, name='glossary'),
    url(r'^logbook$', views.show_logbook, name='logbook'),
    url(r'^propositions$', views.show_propositions, name='propositions'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.logout_user, name='logout'),

]
