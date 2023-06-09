from django.urls import include, path
from rest_framework import routers

from api.views import IngredientViewSet, TagViewSet

router = routers.DefaultRouter()

router.register(r'ingredients',
                IngredientViewSet, basename='ingredient')
router.register(r'tags',
                TagViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls)),
]
