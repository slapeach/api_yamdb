from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
<<<<<<< HEAD
from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail
from reviews.models import User, Title, Review, Comment
from .serializers import UserSerializer, EmailTokenSerializer, ReviewSerializer, CommentSerializer, MyTokenObtainPairSerializer
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import User, Title, Review, Comment, Category, Genre
from .serializers import (UserSerializer, ReviewSerializer,
                          CommentSerializer, TitleSerializer,
                          CategorySerializer, GenreSerializer)
from .permissions import (IsAuthorOrReadOnly, IsUserOrReadOnly,
                          IsModeratorOrReadOnly, IsAdminOrReadOnly,
                          IsSuperUser)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        #'refresh': str(refresh),
        'token': str(refresh.access_token),
    }


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly, IsUserOrReadOnly, IsSuperUser)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class APIsend_code(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        confirmation_code = 1177
        serializer = EmailTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(confirmation_code=confirmation_code)
            send_mail(
               'Регистрация YAMDB',
                f'Для подтверждения регистрации используйте код подвтерждения: {confirmation_code}',
                'yamdb@gmail.com',
                [serializer.data["email"]],
                fail_silently=False
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIsend_token(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = MyTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid() and User.objects.filter(confirmation_code=serializer.data["confirmation_code"]):
            return Response(get_tokens_for_user(request.user), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorOrReadOnly, IsAdminOrReadOnly, IsModeratorOrReadOnly
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        reviews = Review.objects.filter(title_id=title_id)
        review_id = self.kwargs.get('review_id')
        if not review_id:
            return reviews
        return reviews.filter(id=review_id)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.kwargs.get('title_id')
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorOrReadOnly, IsAdminOrReadOnly, IsModeratorOrReadOnly
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        comments = Comment.objects.filter(review_id=review_id)
        comment_id = self.kwargs.get('comment_id')
        if not comment_id:
            return comments
        return comments.filter(id=comment_id)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.kwargs.get('title_id'),
            review_id=self.kwargs.get('review_id')
        )


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre', 'category')


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
