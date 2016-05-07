from django.conf.urls import url, patterns


from . import views

urlpatterns = patterns('',
    url(r'^$', views.GroupDecksList.as_view(), name='group_decks'),
    #url(r'^group_decks/(?P<description>\w+)/$', views.GroupDecksList.as_view(), name='group_decks'),
    url(r'^group_decks/(?P<deck_key>\w+)/$', views.GroupDecksDelete.as_view(), name='group_decks_delete'),
    url(r'^deck_detail/(?P<deck_id>\w+)/$', views.DeckDetail.as_view(), name='deck_detail'),
    url(r'^deck_detail/(?P<deck_id>\w+)/delete/$', views.DeckEdit.as_view(), name='delete_card_from_deck'),
    url(r'^deck_detail/(?P<deck_id>\w+)/add/$', views.DeckEdit.as_view(), name='add_card_to_deck'),
    url(r'^edit_card/(?P<card_id>\w+)/$', views.Edit_Card.as_view(), name='edit_card'),
    url(r'^get_chunk/$', views.get_chunk, name='get_chunk'),
)