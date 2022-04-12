from django.urls import path, include
from rest_framework import routers

from .views import ReviewViewSet

app_name = 'api'


router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)


urlpatterns = [
    path('v1/', include(router.urls)),
]