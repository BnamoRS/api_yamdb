from api.views import CategoryViewSet, GenreViewSet, TitlesViewSet, UserViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include, path

# from rest_framework.authtoken import views

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitlesViewSet)

urlpatterns = [
    path('v1/categories/', include(router_v1.urls)),
    path('v1/users/', include(router_v1.urls)),
    path('v1/genres/', include(router_v1.urls)),
    path('v1/titles/', include(router_v1.urls)),

]
