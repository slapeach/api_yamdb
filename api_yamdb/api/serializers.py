import math
from django.db.models import Avg
from rest_framework import serializers
from django.core.exceptions import ValidationError


from reviews.models import User, Review, Comment, Title, Genre, Category


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер модели User"""

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role'
        )


class EmailTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(message='Данное имя пользователя запрещено')
        if User.objects.filter(username=value).exists():
            raise ValidationError(message=f'Пользователь с username={value} уже существует')


class MyTokenObtainPairSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "confirmation_code")

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise ValidationError(message=f'Пользователь с username={value} отсутствует')
        return value

    def validate_confirmation_code(self, value):
        if not User.objects.filter(confirmation_code=value).exists():
            raise ValidationError(message='Код подтверждения некорректен')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment"""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Title"""
    rating = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(read_only=True)
    genre = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name',
            'year', 'rating',
            'description',
            'genre', 'category'
        )

    def get_rating(self, obj):
        title_id = obj.id
        scores = Review.objects.filter(
            title_id=title_id).aggregate(Avg('score'))
        rating = math.ceil(scores.get('score__avg'))
        return rating


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Genre"""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер модели Category"""

    class Meta:
        model = Category
        fields = ('name', 'slug',)
