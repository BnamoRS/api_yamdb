from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from api.serializers import UserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
