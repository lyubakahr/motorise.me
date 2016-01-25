from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.user_login, name='login'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^create_event', views.create_event, name='create_event'),
    url(r'^delete_event', views.delete_event, name='delete_event'),

    # REST urls start here
    url(r'^user_info$', views.get_user_info, name='user_info'),
    url(r'^user_events$', views.get_user_events, name='user_events'),
    url(r'^all_events$', views.get_all_events, name='all_events'),
    url(r'^event_info$', views.get_event_info, name='event_info'),
    url(r'^all_user_comments$', views.get_all_user_comments, name='all_user_comments'),
    url(r'^all_event_comments$', views.get_all_event_comments, name='all_event_comments')
]