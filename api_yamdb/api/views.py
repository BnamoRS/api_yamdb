from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from reviews.models import Category, Genre, Titles
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from .serializer import CategorySerializer, GenreSerializer, TitlesSerializer
from .permissions import AdminOrReadOnly
from api.serializer import UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
         