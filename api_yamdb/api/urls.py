from api.views import (CategoryViewSet, GenreViewSet,
                       TitlesViewSet, UserViewSet,
                       CreateUserView, CreateTokenView, UserMeView)
from rest_framework.routers import DefaultRouter
from django.urls import include, path


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('v1/users', UserViewSet, basename='users')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitlesViewSet)

urlpatterns = [
    path('v1/categories/', include(router_v1.urls)),
    path('v1/users/', include(router_v1.urls)),
    path('v1/genres/', include(router_v1.urls)),
    path('v1/titles/', include(router_v1.urls)),
    # дописать POST username, email
    path('v1/auth/signup/', CreateUserView.as_view()),
    # POST username end confirmation_code
    path('v1/auth/token/', CreateTokenView.as_view()),
    path('v1/users/me/', UserMeView.as_view()),
    path('', include(router_v1.urls)),

]
