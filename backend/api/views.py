import uuid

from django.db.models import Avg
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import (BlacklistedToken,
                                             OutstandingToken,
                                             RefreshToken,
                                             Token)

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
            response['Content-Disposition'] = 'attachment; filename=%s'%file.name
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
        if self.action in ('set_password', 'me', 'retrieve',):
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

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk=None):
        if request.method == 'DELETE':
            try:
                subscribe = Subscribe.objects.get(siteuser_id=pk)
                if subscribe.is_author(request.user):
                    subscribe.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(
                        {'detail': 'Пользователь не авториУказанной записи нет.'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            except Subscribe.DoesNotExist:
                return Response(
                    {'detail': 'Указанной записи нет.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        if request.method == 'POST':
            print('-->>', 'POST')
        return Response({'ee': 'eeeee'}, status=status.HTTP_400_BAD_REQUEST)


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
