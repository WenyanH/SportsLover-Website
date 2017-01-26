from django.conf.urls import url
from SportsLover import views
import django.contrib.auth.views

 
urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^signup/$', views.registration, name='registration'),
    url(r'^login/$', django.contrib.auth.views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', views.signout, name='logout'),
    url(r'^group/$', views.group, name='group'),
    url(r'^place/$', views.place, name='place'),

    url(r'^profile/(?P<username>\w+)$', views.profile, name='profile'),
    url(r'^profile/$', views.myprofile, name='myprofile'),
    
    url(r'^create_group/$', views.create_group, name='create_group'),
    url(r'^create_confirmation/$', views.create_confirmation, name='create_confirmation'),
    url(r'^group_detail/(?P<id>\d+)$', views.group_detail, name='group_detail'),
    url(r'^setting/$', views.setting, name='setting'),
    url(r'^photo/(?P<id>\d+)$', views.get_photo, name='photo'),
    url(r'^password$', views.password, name='password'),
    url(r'^add-group/$', views.add_group, name='add'),
    url(r'^post-chat/(?P<id>\d+)$', views.post_chat, name='post_chat'),
    url(r'^post-chat/(?P<id>\w+)$', views.post_chat, name='post_chat1'),
    url(r'^post-chat/([\w|\W]+)$', views.post_chat, name='post_chat3'),
    url(r'^group_request/$', views.group_request, name='group_request'),
    url(r'^friend_request/$', views.friend_request, name='friend_request'),
    url(r'^delete-notification-decline-group/(?P<id>\d+)$', views.delete_notification_decline_group, name='delete_notification_decline_group'),
    url(r'^delete-notification-accept-group/(?P<id>\d+)$', views.delete_notification_accept_group, name='delete_notification_accept_group'),
    url(r'^delete-notification-decline-profile/(?P<id>\d+)$', views.delete_notification_decline_profile, name='delete_notification_decline_profile'),
    url(r'^delete-notification-accept-profile/(?P<id>\d+)$', views.delete_notification_accept_profile, name='delete_notification_accept_profile'),
    url(r'^delete-notification-decline-search/(?P<id>\d+)$', views.delete_notification_decline_search, name='delete_notification_decline_search'),
    url(r'^delete-notification-accept-search/(?P<id>\d+)$', views.delete_notification_accept_search, name='delete_notification_accept_search'),
    url(r'^get-joined-group/$', views.get_groups, name='get_groups'),
    url(r'^get-friends/$', views.get_friends, name='get_friends'),
    url(r'^add-chat', views.add_chat),
    url(r'^get-changes/?$', views.get_changes),
    url(r'^get-changes/(?P<time>.+)$', views.get_changes),
    url(r'^get-chats/?$', views.get_chats),
    url(r'^get-chats/(?P<time>.+)$', views.get_chats),
    url(r'^update-news/$', views.update_news, name='update_news'),
    url(r'^delete-news-decline-group/(?P<id>\d+)$', views.delete_news_decline_group, name='delete_news_decline_group'),
    url(r'^delete-news-accept-group/(?P<id>\d+)$', views.delete_news_accept_group, name='delete_news_accept_group'),
    url(r'^delete-news-decline-profile/(?P<id>\d+)$', views.delete_news_decline_profile, name='delete_news_decline_profile'),
    url(r'^delete-news-accept-profile/(?P<id>\d+)$', views.delete_news_accept_profile, name='delete_news_accept_profile'),
    url(r'^delete-news-decline-search/(?P<id>\d+)$', views.delete_news_decline_search, name='delete_news_decline_search'),
    url(r'^delete-news-accept-search/(?P<id>\d+)$', views.delete_news_accept_search, name='delete_news_accept_search'),
    url(r'^friend-chat/(?P<roomname>\w+)$', views.friend_chat, name='friend_chat'),
    url(r'^get-friend-chats/?$', views.get_friend_chats),
    url(r'^get-friends-chats/(?P<time>.+)$', views.get_friend_chats),
    url(r'^get-friend-changes/?$', views.get_friend_changes),
    url(r'^get-friend-changes/(?P<time>.+)$', views.get_friend_changes),
    url(r'^add-friend-chat', views.add_friend_chat),
    url(r'^update-groups/$', views.update_groups, name='update_groups'),
    url(r'^charge/$', views.charge, name="charge"),
    url(r'^get-places/$', views.get_places, name='get_places'),
    url(r'^place-item/(?P<id>\d+)$', views.place_item, name="place_item"),
    url(r'^add-comment/(?P<id>\d+)$', views.add_comment, name="add_comment"),
    url(r'^place-photo/(?P<id>\d+)$', views.get_place_photo, name='place_photo'),
    url(r'^popular-place/$', views.popular_place, name='popular_place'),
    url(r'^recent-sports/$', views.recent_sports, name='recent_sports'),
    url(r'^nearby-places/$', views.nearby_places, name='nearby_places'),
    url(r'^quit-group/(?P<id>\d+)$', views.quit_group, name='quit'),
    url(r'^delete-confirm/(?P<id>\d+)$', views.delete_confirm),
    url(r'^manage-group/$', views.manage_group, name='manage_group'),
    url(r'^update-group-info/(?P<id>\d+)$', views.update_group_info, name='update_group_info'),
    url(r'^update_confirmation/(?P<id>\d+)$', views.update_confirmation, name='update_confirmation'),
]
