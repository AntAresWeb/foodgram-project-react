import uuid

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, views, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.serializers import (
    IngredientSerialiser,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerialiser,
)
from api.filters import IngredientFilter
from essences.models import Ingredient, Recipe, Tag


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerialiser
    permission_classes = (AllowAny,)
    pagination_class = None

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        search_str = self.request.query_params.get('name')
        if search_str is not None:
            queryset = queryset.filter(name__startswith=search_str)
        return queryset


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerialiser
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
#    serializer_class = RecipeSerializer
    permission_classes = (AllowAny, )

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy",):
            permission_classes = (AllowAny,)
#            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (AllowAny,)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy",):
            return RecipeWriteSerializer
        return RecipeReadSerializer
