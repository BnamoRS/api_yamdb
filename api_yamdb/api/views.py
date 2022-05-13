from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from reviews.models import Category, Genre, Titles
from rest_framework import viewsets, generics, permissions
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination
from .serializer import CategorySerializer, GenreSerializer, TitlesSerializer
from .permissions import AdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly

import string
import secrets
from webbrowser import get

from django.core.mail import send_mail

from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdminUserPermission
from api.serializers import (UserSerializer,
                             UserMeSerializer,
                             CreateUserSerializer,
                             CreateTokenSerializer)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminUserPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_class = (AdminOrReadOnly, )
    pagination_class = PageNumberPagination

    # def perform_create(self, serializer):
    #     category = get_object_or_404(


class UserMeView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserMeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        username = self.request.user.username
        obj = get_object_or_404(self.queryset, username=username)
        self.check_object_permissions(self.request, obj)
        return obj


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
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
            serializer.save(confirmation_code=confirmation_code)
            return Response(
                serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTokenView(generics.CreateAPIView):
    #queryset = User.objects.all()
    serialiser_class = CreateTokenSerializer

    def post(self, request):
        #username = request.data.get('username')
        #user = get_object_or_404(User, username=username)
        serializer = CreateTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(
                username=serializer.validated_data.get('username'))
            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)},
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

