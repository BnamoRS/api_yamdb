import email
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'bio', 'role')


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')


class CreateTokenSerializer(serializers.ModelSerializer):
    # Разобраться с проверкой уникальности поля автор
    confirmation_code = serializers.CharField()
    #username = serializers.
    class Meta:
        model = User
        fields = ('confirmation_code',)
