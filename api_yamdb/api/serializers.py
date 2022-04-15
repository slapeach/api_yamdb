import math
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import User, Review, Comment, Title, Genre, Category

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер модели User"""
    username = serializers.SlugField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class EmailTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'confirmation_code')
    
    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Невозможно создать пользователя с таким username'
            )
        return data

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


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Title"""
    rating = serializers.SerializerMethodField()
    rating = serializers.IntegerField()
    category = serializers.StringRelatedField(read_only=True)
    genre = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def get_rating(self, obj):
        title_id = obj.id
        scores = Review.objects.filter(title_id=title_id).aggregate(Avg('score'))
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
