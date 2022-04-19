import string
import secrets
import django_filters
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.decorators import action

from reviews.models import User, Title, Review, Category, Genre
from .serializers import (UserMePatch, UserSerializer, ReviewSerializer,
                          CommentSerializer, TitleSerializer,
                          TitleCreateSerializer, CategorySerializer,
                          GenreSerializer, EmailTokenSerializer,
                          MyTokenObtainPairSerializer
                          )
from .permissions import (IsAdminOrReadOnly,
                          IsAdmin, IsAuthorOrStaffOrReadOnly
                          )
from .mixins import ListCreateDestroyMixin


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    permission_classes = (IsAuthenticated, IsAdmin)
    pagination_class = PageNumberPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('username',)
    search_fields = ['username']

    @action(methods=['get', 'patch'],
            detail=False,
            permission_classes=(IsAuthenticated,),
            url_path='me',)
    def user_data(self, request):
        if request.method == 'GET':
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            user = get_object_or_404(User, username=request.user.username)
            if request.user.role == 'user':
                serializer = UserMePatch(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,
                                    status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = UserSerializer(
                    user, data=request.data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,
                                    status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)


class APIsend_code(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        confirmation_code = ''.join(
            secrets.choice(
                string.ascii_uppercase + string.digits) for _ in range(9))
        serializer = EmailTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                username=request.data['username'],
                confirmation_code=confirmation_code
            )
            send_mail(
                'Регистрация YAMDB',
                f'Для подтверждения регистрации'
                f'используйте код подвтерждения:'
                f'{confirmation_code}',
                'yamdb@gmail.com',
                [serializer.data['email']],
                fail_silently=False
            )
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class APIsend_token(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = MyTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.data.get("username")
        )
        if serializer.data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(request.user).access_token
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(
            {'ошибка авторизации': 'Код подтверждения некорректен'},
            status=status.HTTP_400_BAD_REQUEST)


class ReviewSet(viewsets.ModelViewSet):
    """Вьюсет сериалайзера ReviewSerializer"""
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly & IsAuthorOrStaffOrReadOnly
    ]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('title_id', 'id')

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        author = self.request.user
        if Review.objects.filter(
                author=author, title_id=title_id).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(
                title_id=title_id,
                author=author
            )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет сериалайзера CommentSerializer"""
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly & IsAuthorOrStaffOrReadOnly
    ]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('review_id', 'id',)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user, review=review
        )


class TitleFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = [
            'name', 'year',
            'genre', 'category'
        ]


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет сериалайзера TitleSerializer"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitleCreateSerializer


class CategoryViewSet(ListCreateDestroyMixin):
    """Вьюсет сериалайзера CategorySerializer"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)


class GenreViewSet(ListCreateDestroyMixin):
    """Вьюсет сериалайзера GenreSerializer"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
