import string
import secrets

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from requests import request
from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from api.serializers import UserSerializer, CreateUserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def perform_create(self, serializer):
        alphabet = string.ascii_letters + string.digits
        confirmation_code = ''.join(secrets.choice(alphabet) for i in range(15))
        send_mail(
            'Код подтверждения',
            f'Код подтверждения для POST-запроса: {confirmation_code}',
            '',
            #serializer. data.get('email'),
        )
        return serializer.save(confirmation_code=confirmation_code)
