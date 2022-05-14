from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from reviews.models import Category, Genre, Title
from rest_framework import viewsets, generics, permissions
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination
from .serializer import CategorySerializer, GenreSerializer, TitlesSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

import string
import secrets
from webbrowser import get

from django.core.mail import send_mail

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, permissions, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdminUserPermission
from api.serializer import (
    UserSerializer,
    UserMeSerializer,
    CreateUserSerializer,
    CreateTokenSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from reviews.models import Title

#from .permissions import ReadOnly, IsAuthor, IsModer, IsAdmin


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
    pagination_class = PageNumberPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_class = (IsAdminUserPermission, )
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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = [ReadOnly | IsAuthor | IsModer | IsAdmin]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = [ReadOnly | IsAuthor | IsModer | IsAdmin]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, title=title, review=review)
