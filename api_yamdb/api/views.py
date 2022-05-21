import secrets
import string

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from reviews.models import Category, Genre, Title, User
from api.permissions import (CommentRewiewPermission, IsAdminUserPermission,
                             ReadOnly)
from api.serializer import (CategorySerializer, CommentSerializer,
                            CreateTokenSerializer, CreateUserSerializer,
                            GenreSerializer, ReviewSerializer,
                            TitlesSerializer, UserMeSerializer, UserSerializer)
from api.viewsets import ListOrCreateOrDeleteViewsSet


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminUserPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class CategoryViewSet(ListOrCreateOrDeleteViewsSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdminUserPermission]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListOrCreateOrDeleteViewsSet):
    permission_classes = [ReadOnly | IsAdminUserPermission]
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('id')
    serializer_class = TitlesSerializer
    permission_classes = [ReadOnly | IsAdminUserPermission]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year',)

    def get_queryset(self):
        queryset = self.queryset
        genre_slug = self.request.query_params.get('genre')
        category_slug = self.request.query_params.get('category')
        name = self.request.query_params.get('name')
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


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
    serialiser_class = CreateTokenSerializer

    def post(self, request):
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
    pagination_class = PageNumberPagination
    permission_classes = [CommentRewiewPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all().order_by('pub_date')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [CommentRewiewPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        return review.comments.all().order_by('pub_date')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
