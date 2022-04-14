from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
<<<<<<< HEAD
from rest_framework import viewsets

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail


from rest_framework.pagination import LimitOffsetPagination

from reviews.models import User, Title, Review, Comment
from .serializers import UserSerializer,EmailTokenSerializer, ReviewSerializer, CommentSerializer
=======
from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import User, Title, Review, Comment, Category, Genre
from .serializers import (UserSerializer, ReviewSerializer,
                          CommentSerializer, TitleSerializer,
                          CategorySerializer, GenreSerializer)
>>>>>>> master
from .permissions import (IsAuthorOrReadOnly,
                          IsModeratorOrReadOnly, IsAdminOrReadOnly)
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет сериалайзера UserSerializer"""
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


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorOrReadOnly, IsAdminOrReadOnly, IsModeratorOrReadOnly
    ]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title_id', 'review_id']

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.kwargs.get('title_id')
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorOrReadOnly, IsAdminOrReadOnly, IsModeratorOrReadOnly
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title_id', 'review_id', 'comment_id']

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.kwargs.get('title_id'),
            review_id=self.kwargs.get('review_id')
        )


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    pass


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]



class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
