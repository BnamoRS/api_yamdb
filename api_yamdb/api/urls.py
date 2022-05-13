from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views import UserViewSet, UserMeView, CreateUserView, CreateTokenView, CommentViewSet, ReviewViewSet


router_v1 = routers.DefaultRouter()


router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)


urlpatterns = [
    path('v1/auth/signup/', CreateUserView.as_view()),
    path('v1/auth/token/', CreateTokenView.as_view()),
    path('v1/users/me/', UserMeView.as_view()),
    path('v1/', include(router_v1.urls)),
]
