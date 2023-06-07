from django.urls import include, path
from rest_framework import routers

from users import views

router = routers.DefaultRouter()

router.register(r'users/me/', views.CommentViewSet, basename='comment')
router.register(r'users/me/', views.CommentViewSet, basename='comment')
router.register(r'users/(?P<id>\d+)/', views.CommentViewSet, basename='comment')
router.register('users/', views.UserViewSet, basename='user')

urlpatterns = [
    path('auth/signup/', views.AuthSignupView.as_view(), name='signup'),
    path('auth/token/', views.AuthTokenView.as_view(), name='token'),
    path('users/me/',
         views.UserMeDetailUpdateAPIView.as_view(), name='userme'),
    path('drf-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
