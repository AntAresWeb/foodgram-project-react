import uuid

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, views, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (UserListSerializer,
                          UserMeSerializer,
                          UserSignupSerializer,
                          UserSerializer,
                          UserTokenSerializer)


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
#    filter_backends = (filters.SearchFilter,)
#    lookup_field = 'username'
#    search_fields = ('username',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserListSerializer
        elif self.request.method == 'POST':
            return UserSerializer


class UserProfileViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)

    def get_serializer(self):
        if self.request.method == 'GET':
            return UserListSerializer
        else:
            return UserSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            return User.objects.subscribe.exist()
        else:
            return User.objects.all()


class SetPasswordView(views.APIView):
    ...


class TokenLoginView(views.APIView):
    ...


class TokenLogoutView(views.APIView):
    ...


class UserMeViewSet(mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserMeSerializer
    lookup_field = 'username'

    def get(self, request):
        instance = get_object_or_404(User, pk=request.user.id)
        serializer = self.serializer_class(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        instance = get_object_or_404(User, pk=request.user.id)
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthSignupView(views.APIView):
    serializer_class = UserSignupSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        response = {}
        for field in ('username', 'email'):
            if field not in request.data:
                response[field] = ['Обязательное поле.']
        if len(response) > 0:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)
                if email != user.email:
                    response['email'] = ['Не совпадает с регистрационным.']
                    return Response(response,
                                    status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                if User.objects.filter(email=email).exists():
                    response['email'] = ['Такой e-mail уже занят.']
                    return Response(response,
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = User.objects.create(username=username, email=email)
            user.confirmation_code = str(uuid.uuid4())
            user.save()
            send_mail('Авторизация в YaMDB',
                      f'''
                      Уважаемый {user.username}!
                      Вы успешно прошли регистрацию на сервисе YaMDB.
                      Высылаем вам код активаци для получения токена:
                      {user.confirmation_code}
                      ''',
                      'admin@yamdb',
                      (user.email,),
                      fail_silently=False,)

            status_code = status.HTTP_200_OK
            return Response(serializer.validated_data, status=status_code)


class AuthTokenView(views.APIView):
    serializer_class = UserTokenSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        response = {}
        if 'username' not in request.data:
            response['username'] = ['Обязательное поле.']
        if 'confirmation_code' not in request.data:
            response['confirmation_code'] = ['Обязательное поле.']
        if len(response) > 0:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            user = get_object_or_404(User, username=username)
            if confirmation_code != user.confirmation_code:
                response['confirmation_code'] = ['Неверный код подтверждения.']
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            status_code = status.HTTP_200_OK
            response = {
                'token': token
            }

            return Response(response, status=status_code)
