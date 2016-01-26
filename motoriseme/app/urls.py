from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.user_login, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^create_event$', views.create_event, name='create_event'),
    url(r'^read_all_events$', views.read_all_events, name='read_all_events'),
    url(r'^read_user_events$', views.read_user_events, name='read_user_events'),
    url(r'^read_event$', views.read_event, name='read_event'),
    url(r'^update_event$', views.update_event, name='update_event'),
    url(r'^delete_event$', views.delete_event, name='delete_event'),
    url(r'^user_info$', views.get_user_info, name='user_info'),
    url(r'^get_rider$', views.get_rider, name='get_rider'),
    url(r'^update_rider$', views.update_rider, name='update_rider'),
    url(r'^all_user_comments$', views.get_all_user_comments, name='all_user_comments'),
    url(r'^all_event_comments$', views.get_all_event_comments, name='all_event_comments'),
    url(r'^post_comment$', views.post_comment, name='post_comment'),
    url(r'^edit_comment$', views.edit_comment, name='edit_comment'),
    url(r'^delete_comment$', views.delete_comment, name='delete_comment'),
    url(r'^create_notification$', views.create_notification, name='create_notification'),
    url(r'^read_user_notifications$', views.read_user_notifications, name='read_user_notifications'),
    url(r'^set_notification_seen$', views.set_notification_seen, name='set_notification_seen'),
    url(r'^get_notification_types$', views.get_notification_types, name='get_notification_types'),
    url(r'^get_moto_types$', views.get_motorbike_types, name='get_moto_types'),
    url(r'^get_moto_manufacturers$', views.get_motorbike_manufacturers, name='get_moto_manufacturers'),
]

