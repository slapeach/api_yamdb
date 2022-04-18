import string
import secrets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from rest_framework.response import Response
from django.core.mail import send_mail


from reviews.models import User, Title, Review, Comment
from .serializers import (UserSerializer, EmailTokenSerializer,
                          ReviewSerializer, CommentSerializer,
                          MyTokenObtainPairSerializer)
from rest_framework import viewsets, mixins
from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import PageNumberPagination


from reviews.models import User, Title, Review, Comment, Category, Genre
from .serializers import (UserSerializer, ReviewSerializer,
                          CommentSerializer, TitleSerializer,
                          TitleCreateSerializer, CategorySerializer,
                          GenreSerializer)
from .permissions import (IsAuthorOrReadOnly, IsUserOrReadOnly,
                          IsModeratorOrReadOnly, IsAdminOrReadOnly,
                          IsAdmin)
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly, )
    pagination_class = PageNumberPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('username',)
    search_fields = ['username']

    def retrieve(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class APIsend_code(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        confirmation_code = ''.join(
            secrets.choice(
                string.ascii_uppercase + string.digits) for _ in range(9))
        serializer = EmailTokenSerializer(data=request.data)
        if request.data.get('username') == 'me':
            return Response('Данное имя пользователя запрещено',
                            status=status.HTTP_400_BAD_REQUEST)
        elif serializer.is_valid():
            serializer.save(confirmation_code=confirmation_code)
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
        user = get_object_or_404(User, username=serializer.data.get("username"))
        if serializer.data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(request.user).access_token
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response({'ошибка авторизации': 'Код подтверждения некорректен'},
                        status=status.HTTP_400_BAD_REQUEST)


class APIPatch_me(APIView):
    permission_classes = (IsAuthenticated, IsUserOrReadOnly, IsAdminOrReadOnly)
 
    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly]
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
    permission_classes = [IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre', 'category')
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitleCreateSerializer


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
