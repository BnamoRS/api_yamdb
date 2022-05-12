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
    
    def validate_confirmation_code(self, value):
        #print(value)
        #print(self.instance.confirmation_code)

        if self.instance.confirmation_code != value:
            raise serializers.ValidationError('Неверный код подтверждения')
        return value
        
    class Meta:
        model = User
        fields = ('confirmation_code',)
