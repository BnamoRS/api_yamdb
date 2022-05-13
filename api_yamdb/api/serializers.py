from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Review, Comment


User = get_user_model()


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
            'username', 'first_name', 'last_name', 'email', 'bio', 'role'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        
