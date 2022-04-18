from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from .views import (ReviewViewSet, CommentViewSet,
                    UserViewSet, GenreViewSet,
                    CategoryViewSet, TitleViewSet,
                    APIsend_code, APIsend_token, APIPatch_me)

app_name = 'api'


router = routers.DefaultRouter()
r = router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(r'users', UserViewSet, basename='user')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/auth/signup/', APIsend_code.as_view()),
    path('v1/auth/token/', APIsend_token.as_view(), name='token_obtain_pair'),
    #path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/users/me', APIPatch_me.as_view()),
    path('v1/', include(router.urls)),
]
