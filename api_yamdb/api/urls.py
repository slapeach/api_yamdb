from django.urls import path, include
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet, UserViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (ReviewViewSet, CommentViewSet,
                    UserViewSet, GenreViewSet,
                    CategoryViewSet, TitleViewSet,
                    APIsend_code)


app_name = 'api'


router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(r'users', UserViewSet)
<<<<<<< HEAD
#router.register(r'auth/signup', send_code, basename='confirmation_code')
=======
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)
>>>>>>> master


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup', APIsend_code.as_view()),
    path('v1/auth/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
