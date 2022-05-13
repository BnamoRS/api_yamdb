from api.views import (CategoryViewSet, GenreViewSet,
                       TitlesViewSet, UserViewSet,
                       CreateUserView, CreateTokenView, UserMeView)
from rest_framework.routers import DefaultRouter
from django.urls import include, path


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('v1/categories', CategoryViewSet)
router_v1.register('v1/genres', GenreViewSet)
router_v1.register('v1/titles', TitlesViewSet)

urlpatterns = [
    path('categories/', include(router_v1.urls)),
    path('users/', include(router_v1.urls)),
    path('genres/', include(router_v1.urls)),
    path('titles/', include(router_v1.urls)),
    # дописать POST username, email
    path('v1/auth/signup/', CreateUserView.as_view()),
    # POST username end confirmation_code
    path('v1/auth/token/', CreateTokenView.as_view()),
    path('v1/users/me/', UserMeView.as_view()),
    path('', include(router_v1.urls)),

]
