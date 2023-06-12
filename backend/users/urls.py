from django.urls import include, path
from rest_framework import routers

from users import views

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('auth/token/login/', views.TokenLoginView.as_view(), name='login'),
    path('auth/token/logout/', views.TokenLogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
