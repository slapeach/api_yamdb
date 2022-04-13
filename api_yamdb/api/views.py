from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail

from reviews.models import User, Title, Review
from .serializers import UserSerializer, ReviewSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет сериалайзера UserSerializer"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def send_code(self,request):
    serializer = UserSerializer(data=request.data)
    confirmation_code = 111777111777
    if serializer.is_valid():
        serializer.save()
        send_mail(
            'Регистрация YAMDB',
            f'Для подтверждения регистрации используйте код подвтерждения: {confirmation_code}',
            'yamdb@gmail.com',
            [request.user.email],
            fail_silently=False
        )


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly & IsOwnerOrReadOnly]

    def get_qieryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        queryset = title.review.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.kwargs.get('title_id')
        )


class CommentViewSet(viewsets.ModelViewSet):
    pass
