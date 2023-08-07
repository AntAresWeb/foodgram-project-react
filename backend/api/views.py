import csv

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import (BlacklistedToken,
                                             OutstandingToken,
                                             RefreshToken,
                                             Token)

from api.filters import (
    TagsFilterBackend,
    FavoritedFilterBackend,
)
from essences.models import (
    Content, Favorite, Ingredient, Recipe, Shoppingcart, Subscribe, Tag, User
)
from api.permissions import IsAuthor
from api.serializers import (
    IngredientSerialiser,
    RecipeReadSerializer,
    RecipeShortSerializer,
    RecipeWriteSerializer,
    SubscribeSerializer,
    TagSerialiser,
)
from core.permissions import IsTokenValid
from .serializers import (LoginSerializer,
                          PasswordSerializer,
                          UserListSerializer,
                          UserSerializer)


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
    filter_backends = (
        TagsFilterBackend,
        FavoritedFilterBackend,
    )

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update',
                           'destroy', 'favorite', 'shopping_cart',
                           'download_shopping_cart',):
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
        user = request.user
        qs_recipes = user.shoppingcarts.values('recipe')
        qs_contents = Content.objects.filter(
            recipe__in=qs_recipes).select_related('ingredient')
        shopping_list = qs_contents.values(
            'ingredient__name',
            'ingredient__measurement_unit').annotate(
                amount=Sum('amount')).order_by('ingredient__name')

        response = HttpResponse(
            content_type='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename="shopinglist.csv"'
            },
        )

        writer = csv.writer(response)
        writer.writerow(['Список покупок'])
        for item in shopping_list:
            writer.writerow((item['ingredient__name'],
                             item['ingredient__measurement_unit'],
                             item['amount'],))
        return response

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'DELETE':
            try:
                Shoppingcart.objects.get(siteuser=user, recipe=recipe).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Shoppingcart.DoesNotExist:
                return Response(
                    {'detail': 'В корзине этого рецепта нет.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'POST':
            try:
                favorite = Shoppingcart.objects.get(
                    siteuser=user, recipe=recipe)
                return Response(
                    {'detail': 'Этот рецепт уже есть в корзине.'},
                    status=status.HTTP_400_BAD_REQUEST)
            except Shoppingcart.DoesNotExist:
                favorite = Shoppingcart.objects.create(
                    siteuser=user, recipe=recipe)
                serialiser = RecipeShortSerializer(
                    instance=favorite.recipe, many=False)
                return Response(serialiser.data,
                                status=status.HTTP_201_CREATED)

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'DELETE':
            try:
                Favorite.objects.get(siteuser=user, recipe=recipe).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Favorite.DoesNotExist:
                return Response(
                    {'detail': 'Этого рецепта нет в избранных.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'POST':
            try:
                favorite = Favorite.objects.get(siteuser=user, recipe=recipe)
                return Response(
                    {'detail': 'Этот рецепт уже есть в избранных.'},
                    status=status.HTTP_400_BAD_REQUEST)
            except Favorite.DoesNotExist:
                favorite = Favorite.objects.create(
                    siteuser=user, recipe=recipe)
                serialiser = RecipeShortSerializer(
                    instance=favorite.recipe, many=False)
                return Response(serialiser.data,
                                status=status.HTTP_201_CREATED)

# Раздел пользовательской модели api/users/


class UserViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserListSerializer
        elif self.request.method == 'POST':
            return UserSerializer

    def get_permissions(self):
        if self.action in ('set_password', 'me', 'retrieve', 'subscribe'):
            permission_classes = (IsAuthenticated, IsTokenValid,)
        else:
            permission_classes = (AllowAny,)
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def me(self, request):
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            if user.check_password(
               serializer.validated_data['current_password']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
            else:
                return Response(
                    {'detail': 'Учетные данные не были предоставлены'},
                    status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def prepare_context(self):
        context = {'request': self.request}
        recipes_limit = self.request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            try:
                context['recipes_limit'] = int(recipes_limit)
            except ValueError:
                context['recipes_limit'] = 0
        return context

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, id=pk)

        if request.method == 'DELETE':
            try:
                Subscribe.objects.get(siteuser=user, author=author).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Subscribe.DoesNotExist:
                return Response(
                    {'detail': 'Нет подписки на этого пользователя.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'POST':
            if pk == user.id:
                return Response(
                    {'detail': 'Нельзя подписаться на себя.'},
                    status=status.HTTP_400_BAD_REQUEST)
            try:
                subscribe = Subscribe.objects.get(siteuser=user, author=author)
                return Response(
                    {'detail': 'Подписка уже есть.'},
                    status=status.HTTP_400_BAD_REQUEST)
            except Subscribe.DoesNotExist:
                subscribe = Subscribe.objects.create(
                    siteuser=user, author=author)
                serialiser = SubscribeSerializer(
                    instance=subscribe, context=self.prepare_context
                )
                return Response(serialiser.data,
                                status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        serialiser = SubscribeSerializer(many=True)
        return Response(serialiser.data, status=status.HTTP_200_OK)


class TokenLoginView(views.APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User,
                                     email=serializer._validated_data['email'])
            password = serializer.validated_data['password']
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                access = str(refresh.access_token)
                return Response(
                    {'auth_token': access}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenLogoutView(views.APIView):
    serializer_class = None
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.user.is_authenticated:
            for token in OutstandingToken.objects.filter(user=request.user):
                BlacklistedToken.objects.get_or_create(token=token)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'detail': 'Учетные данные не были предоставлены.'},
                status=status.HTTP_401_UNAUTHORIZED)
