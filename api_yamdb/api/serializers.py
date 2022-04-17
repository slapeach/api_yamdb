import math
import datetime
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.core.exceptions import ValidationError

from reviews.models import User, Review, Comment, Title, Genre, Category


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер модели User"""
    username = serializers.SlugField()

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
            raise ValidationError(
                message=f'Пользователь с username={value} уже существует'
            )


class MyTokenObtainPairSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise ValidationError(
                message=f'Пользователь с username={value} отсутствует'
            )
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

    def validate_author(self, value):
        if Review.objects.filter(author=value).exists():
            raise ValidationError(
                message='Возможно оставить только один отзыв'
            )
        if self.request.user.username != value:
            raise ValidationError(
                message='Отзыв можно оставить только от своего имени'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment"""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Genre"""
    # slug = serializers.SlugField()

    class Meta:
        model = Genre
        fields = ('name', 'slug')

class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер модели Category"""
    # slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = ('name', 'slug',)

class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Title"""
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(required=True, many=True)
    category = CategorySerializer(required=True)

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
        reviews = Review.objects.filter(title_id=title_id)
        if reviews.count() > 0:
            scores = reviews.aggregate(Avg('score'))
            rating = math.ceil(scores.get('score__avg'))
            return rating
        return 0

    def validate_year(self, value):
        now = datetime.datetime.now()
        if value > now.year:
            raise ValidationError(message='Укажите корректный год выпуска')
        return value


class PostTitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'name', 'year',
            'description', 'genre',
            'category'
        )