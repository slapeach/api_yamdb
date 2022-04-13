from rest_framework import serializers

from reviews.models import User, Review, Comment, Title, Genre, Category


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер модели User"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class ReviewSerializer(serializers.ModelSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Title"""

    class Meta:
        model = Title
        fields = ()


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Genre"""
    pass


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер модели Category"""
    pass