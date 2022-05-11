from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views import UserViewSet, CreateUserView


router_v1 = routers.DefaultRouter()


router_v1.register('v1/users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/auth/signup/', CreateUserView.as_view()), # дописать POST username, email
    # path('v1/auth/token/',), # POST username end confirmation_code
    path('', include(router_v1.urls)),
]
