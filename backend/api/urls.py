from django.urls import include, path
from rest_framework import routers

from api.views import IngredientViewSet

router = routers.DefaultRouter()

router.register(r'ingredients',
                IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls)),
]
