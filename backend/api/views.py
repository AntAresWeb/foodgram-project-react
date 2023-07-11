import uuid

from django.db.models import Avg
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter
from essences.models import (
    Content, Favorite, Ingredient, Recipe, Shoppingcart, Subscribe, Tag, User
)
from api.permissions import IsAuthor
from api.serializers import (
    IngredientSerialiser,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerialiser,
)
from essences.models import (
    Content, Favorite, Ingredient, Recipe, Shoppingcart, Subscribe, Tag, User
)


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
    permission_classes = (AllowAny, )

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy",):
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (AllowAny,)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy',):
            return RecipeWriteSerializer
        return RecipeReadSerializer

    @action(methods=['GET'], detail=False, url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        with open('file.csv', 'r') as file:
            response = HttpResponse(file, content_type='application/msword')
            response['Content-Disposition'] = 'attachment; filename=%s' %file.name
        return response

    @action(methods=['POST', 'DELETE'], detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        print('recipe -->>', recipe)
        print('user -->>', request.user)
        print('self.action -->>', repr(self.action))
        if self.action in ('destroy',):
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if self.action in ('post',):
            shopping_cart = Shoppingcart.objects.create(
                siteuser=request.user, recipe=recipe)
            shopping_cart.save()
            return Response({'message': 'shopping_cart'},
                            status=status.HTTP_200_OK)
