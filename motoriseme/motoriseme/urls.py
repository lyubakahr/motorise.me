from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from app import views
import rest_framework


router = routers.DefaultRouter()
router.register(r'users', views.RiderViewSet)

urlpatterns = [
	# url(r'^', include(router.urls)),
	# url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('app.urls')),
    url(r'^admin/', admin.site.urls),
]