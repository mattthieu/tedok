from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^up_visibility/(?P<item_id>\d+)/(?P<nb_votes>\d+)/$',
        views.up_visibility, name='up_visibility'),
    url(r'^down_visibility/(?P<item_id>\d+)/(?P<nb_votes>\d+)/$',
        views.down_visibility, name='down_visibility'),
    url(r'^manifesti$', views.show_manifesti, name='manifesti'),
    url(r'^add_value/$', views.ValueCreate.as_view(), name='add_value'),
    url(r'^edit_value/(?P<pk>[0-9]+)/$',
        views.ValueUpdate.as_view(), name='edit_value'),
    url(r'^add_logbookpost/$',
        views.LogbookpostCreate.as_view(), name='add_logbookpost'),
    url(r'^edit_logbookpost/(?P<pk>[0-9]+)/$',
        views.LogbookpostUpdate.as_view(), name='edit_logbookpost'),
    url(r'^add_glossaryword/$',
        views.GlossaryWordCreate.as_view(), name='add_glossaryword'),
    url(r'^edit_glossaryword/(?P<pk>[0-9]+)/$',
        views.GlossaryWordUpdate.as_view(), name='edit_glossaryword'),
    url(r'^add_proposition/$',
        views.PropositionCreate.as_view(), name='add_proposition'),
    url(r'^edit_proposition/(?P<pk>[0-9]+)/$',
        views.PropositionUpdate.as_view(), name='edit_proposition'),
    url(r'^updown_proposition/(?P<proposition_id>\d+)/' +
        '(?P<vote>\d+)/$',
        views.updown_proposition, name='updown_proposition'),
    url(r'^ressources$', views.show_ressources, name='ressources'),
    url(r'^glossary$', views.show_glossary, name='glossary'),
    url(r'^logbook$', views.show_logbook, name='logbook'),
    url(r'^propositions$', views.show_propositions, name='propositions'),
]
