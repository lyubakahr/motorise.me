from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.user_login, name='login'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^create_event', views.create_event, name='create_event'),
    url(r'^delete_event', views.delete_event, name='delete_event'),
    url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
]