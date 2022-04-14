from django.urls import path, include
from rest_framework import routers

from .views import (ReviewViewSet, CommentViewSet,
                    UserViewSet, GenreViewSet,
                    CategoryViewSet, TitleViewSet)

app_name = 'api'


router = routers.DefaultRouter()
r = router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)',
    CommentViewSet, basename='comments'
)
router.register(r'users', UserViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
