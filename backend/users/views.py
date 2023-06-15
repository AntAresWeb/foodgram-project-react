import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (LoginSerializer,
                          PassordSerializer,
                          UserListSerializer,
                          UserSignupSerializer,
                          UserSerializer,
                          UserTokenSerializer)


class UserViewSet(mixins.CreateModelMixin,
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

    @action(detail=False, methods=['get'])
    def me(self, request):
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        user = get_object_or_404(User, pk=4)
        serializer = PassordSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data['current_password'])
            print(serializer.validated_data['new_password'])
            if user.check_password(
               serializer.validated_data['current_password']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
            else:
                return Response(
                    {'detail': 'Учетные данные не были предоставлены'},
                    status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenLoginView(views.APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User,
                                     email=serializer._validated_data['email'])
            if user.check_password(
               serializer.validated_data['password']):
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                return Response(
                    {'auth_token': token}, status=status.HTTP_201_CREATED)


class TokenLogoutView(views.APIView):
    serializer_class = None
    permission_classes = (AllowAny, )

    def post(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, pk=request.user.id)
            RefreshToken.for_user(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

