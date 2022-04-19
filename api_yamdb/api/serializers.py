import math
import datetime
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
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


class UserMePatch(serializers.ModelSerializer):
    """Сериалайзер модели User"""
    username = serializers.SlugField()
    role = serializers.CharField(read_only=True)

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


class MyTokenObtainPairSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=40, required=True)
    confirmation_code = serializers.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""
    author = SlugRelatedField(read_only=True, slug_field='username')
    title = SlugRelatedField(
        write_only=True, queryset=Title.objects.all(),
        slug_field='title', required=False
    )

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
        title = get_object_or_404(
            Title, id=self.context['view'].kwargs.get('title_id')
        )
        user = self.context.get('request').user
        if Review.objects.filter(title=title, author=user).exists():
            if self.context['request'].method in ['POST']:
                raise serializers.ValidationError(
                    'Возможно оставить только 1 отзыв на произведение'
                )
        return super().validate(attrs)


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
            raise ValidationError(message='Укажите корректный год выпуска')
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
