from django.contrib.auth import get_user_model
from rest_framework import serializers
from reviews.models import Category, Genre, Titles
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'category', 'genre')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role')


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'bio', 'role')


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать << username>>: << me >>')
        return value


class CreateTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField()
    username = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        if user.confirmation_code != data.get('confirmation_code'):
            raise serializers.ValidationError('Неверный код подтверждения')
        return data

    class Meta:
        model = User
        fields = ('confirmation_code', 'username')
