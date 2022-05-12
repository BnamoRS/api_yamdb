import string
import secrets

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from requests import request
from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view

from api.permissions import IsAdminUserPermission
from api.serializers import (
    UserSerializer, CreateUserSerializer, CreateTokenSerializer)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUserPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def perform_create(self, serializer):
        alphabet = string.ascii_letters + string.digits
        confirmation_code = ''.join(
            secrets.choice(alphabet) for i in range(15))
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        send_mail(
            'Код подтверждения регистрации YAMDB',
            f'Код подтверждения для пользователя <<{username}>>:'
            f' {confirmation_code}',
            '',
            (email,),
        )
        return serializer.save(confirmation_code=confirmation_code)


class CreateTokenView(generics.CreateAPIView):
    #queryset = User.objects.all()
    serialiser_class = CreateTokenSerializer

    def post(self, request):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        serializer = CreateTokenSerializer(user, data=request.data)
        if serializer.is_valid():
            token = RefreshToken.for_user(request.user)
            return Response(
                {'token': str(token.access_token)},
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
