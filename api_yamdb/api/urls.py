from django.urls import path, include
from rest_framework import routers

from api.views import UserViewSet


router_v1 = routers.DefaultRouter()


router_v1.register('v1/users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router_v1.urls)),
]
