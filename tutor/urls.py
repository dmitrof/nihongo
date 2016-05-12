from django.conf.urls import url, patterns


from . import views

urlpatterns = patterns('',
                       #url(r'^tutor_groups_list/(?P<user_uid>\w+)/$', views.TutorGroupsList.as_view(), name='tutor_groups_list'),
                    url(r'^$', views.TutorGroupsList.as_view(), name='tutor_groups'),

                    url(r'^tutor_groups_list/$', views.TutorGroupsList.as_view(), name='tutor_groups'),
                    url(r'^tutor_groups_list/(?P<user_id>\w+)/(?P<group_id>\w+)/$', views.request_invite, name='request_invite'),
                    url(r'^confirm_ir/(?P<ir_id>\w+)/(?P<group_id>\w+)/(?P<user_id>\w+)/$', views.confirm_ir, name='confirm_ir'),

                    url(r'^group_decks/(?P<group_id>\w+)/$', views.GroupDecksList.as_view(), name='group_decks'),
                    #url(r'^group_decks/(?P<description>\w+)/$', views.GroupDecksList.as_view(), name='group_decks'),
                    url(r'^group_decks/(?P<group_id>\w+)/(?P<deck_id>\w+)/$', views.GroupDecksDelete.as_view(), name='group_decks_delete'),
                    url(r'^deck_detail/(?P<group_id>\w+)/(?P<deck_id>\w+)/$', views.DeckDetail.as_view(), name='deck_detail'),
                    url(r'^deck_edit/(?P<group_id>\w+)/(?P<deck_id>\w+)/$', views.DeckEdit.as_view(), name='deck_edit'),
                    #url(r'^deck_detail/(?P<deck_id>\w+)/add/$', views.DeckEdit.as_view(), name='add_card_to_deck'),
                    url(r'^edit_card/(?P<group_id>\w+)/(?P<deck_id>\w+)/(?P<card_id>\w+)/$', views.EditCard.as_view(), name='edit_card'),
                    url(r'^edit_card/(?P<group_id>\w+)/(?P<deck_id>\w+)/(?P<card_id>\w+)/(?P<is_new>\w+)/$', views.EditCard.as_view(), name='edit_card'),
                    url(r'^edit_card/(?P<group_id>\w+)/(?P<deck_id>\w+)/(?P<card_id>\w+)/(?P<is_new>\w+)/(?P<task_type>\w+)/$', views.EditCard.as_view(), name='edit_card'),
                    url(r'^edit_card/(?P<group_id>\w+)/(?P<card_id>\w+)/$', views.EditCard.as_view(), name='save_card'),
                    url(r'^get_chunk/$', views.get_chunk, name='get_chunk'),
                )

