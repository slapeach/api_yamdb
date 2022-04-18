import math
import datetime
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

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
        fields = ('username', 'confirmation_code')

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
    author = SlugRelatedField(read_only=True, slug_field='username')
    title = SlugRelatedField(
        write_only=True, queryset=Title.objects.all(),
        slug_field='title', required=False
    )
    text = serializers.CharField(allow_blank=False)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')

    def validate_author(self, value):
        if self.request.user.username != value:
            raise ValidationError(
                message='Отзыв можно оставить только от своего имени'
            )
        return value

    def validate(self, attrs):
        title = get_object_or_404(Title, id=self.context['view'].kwargs.get('title_id'))
        user = self.context.get('request').user
        if Review.objects.filter(title=title, author=user).exists():
            if self.context['request'].method in ['POST']:
                raise serializers.ValidationError('Только один отзыв от пользователя')
        return super().validate(attrs)
'''
    def validate_score(self, value):
        if value < 1 or value > 10:
            raise ValidationError(
                message='Возможная оценка: от 1 до 10'
            )
'''

class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment"""
    author = SlugRelatedField(read_only=True, slug_field='username')
    review = SlugRelatedField(
        write_only=True, queryset=Review.objects.all(),
        slug_field='review', required=False
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Genre"""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер модели Category"""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Title"""
    rating = serializers.SerializerMethodField(read_only=True)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

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
        return None

    def validate_year(self, value):
        now = datetime.datetime.now()
        if value > now.year:
            raise ValidationError(message=f'Укажите корректный год выпуска')
        return value


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
