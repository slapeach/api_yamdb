from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import User, Title, Review, Comment
from .serializers import UserSerializer, ReviewSerializer, CommentSerializer
from .permissions import (IsAuthorOrReadOnly,
                          IsModeratorOrReadOnly, IsAdminOrReadOnly)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorOrReadOnly, IsAdminOrReadOnly, IsModeratorOrReadOnly
    ]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title_id']

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
    filterset_fields = ['review_id']

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.kwargs.get('title_id'),
            review_id=self.kwargs.get('review_id')
        )


class TitleViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass
