from datetime import timedelta
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import (BlacklistedToken,
                                             OutstandingToken,
                                             RefreshToken,
                                             Token)
from core.permissions import IsTokenValid
from .models import User
from .serializers import (LoginSerializer,
                          PasswordSerializer,
                          UserListSerializer,
                          UserSerializer)


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
            logout(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'detail': 'Учетные данные не были предоставлены.'},
                status=status.HTTP_401_UNAUTHORIZED)
