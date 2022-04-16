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
                          CategorySerializer, GenreSerializer)
from .permissions import (IsAuthorOrReadOnly, IsUserOrReadOnly,
                          IsModeratorOrReadOnly, IsAdminOrReadOnly,
                          IsSuperUser)
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.views import APIView


from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    permission_classes = (IsAdminOrReadOnly,
                          IsUserOrReadOnly, IsSuperUser)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class APIsend_code(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        confirmation_code = str(
            RefreshToken.for_user(request.user).access_token)[:9]
        serializer = EmailTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(username=request.data['username'], confirmation_code=confirmation_code)
            send_mail(
                'Регистрация YAMDB',
                f'Для подтверждения регистрации используйте код подвтерждения:'
                f'{confirmation_code}',
                'yamdb@gmail.com',
                [serializer.data["email"]],
                fail_silently=False
            )
            return Response(serializer.data['confirmation_code'],
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        #elif 'email' not in serializer.data and 'username' not in serializer.data:
        #    return Response("Введите корректные данные", status=status.HTTP_400_BAD_REQUEST)
        #elif User.objects.filter(
                #username=serializer.data["username"]).count() > 1:
        #elif get_object_or_404(User, username=serializer.validated_data["username"]).count() > 1:
         #   return Response("пользователь с таким именем уже существует",
         #                   status=status.HTTP_400_BAD_REQUEST)
        #elif serializer.data['username'] == 'me':
         #   return Response("Данный username запрещен",
         #                   status=status.HTTP_400_BAD_REQUEST)



class APIsend_token(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = MyTokenObtainPairSerializer(data=request.data)
        #serializer.is_valid(raise_exception=False)
        token = RefreshToken.for_user(request.user)
        if User.objects.filter(confirmation_code=request.data['confirmation_code']).all().exists():
            return Response({'token': str(token.access_token)},
                            status=status.HTTP_201_CREATED)
        else:
            return Response('ошибка',
                            status=status.HTTP_400_BAD_REQUEST)


class APIsend_token111(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = MyTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(
                username=serializer.validated_data["username"]
            )
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if (
            serializer.validated_data["confirmation_code"]
            == user.confirmation_code
        ):
            token = RefreshToken.for_user(request.user).access_token
            return Response(
                {"token": str(token)},
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = [IsAuthenticatedOrReadOnly]
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
