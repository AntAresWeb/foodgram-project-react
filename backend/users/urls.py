from django.urls import include, path
from rest_framework import routers

from users import views

router = routers.DefaultRouter()

router.register(r'users/me', views.UserMeViewSet, basename='user_me')
router.register(r'users/(?P<id>\d+)',
                views.UserProfileViewSet, basename='user_profile')
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('users/set_password/',
         views.SetPasswordView.as_view(), name='set_password'),
    path('auth/token/login/', views.TokenLoginView.as_view(), name='login'),
    path('auth/token/logout/', views.TokenLogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
