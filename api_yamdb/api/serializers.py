import math
import datetime
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


class MyTokenObtainPairSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


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
