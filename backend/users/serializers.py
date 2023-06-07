from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import User
from .utils import name_is_valid


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed',)


class UserSerializer(serializers.ModelSerializer):
    '''Сериализер api/v1/users/'''

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = 'username'
        extra_kwargs = {
            'email': {'required': True, 'max_length': 254},
            'username': {'required': True, 'max_length': 150},
            'first_name': {'required': True, 'max_length': 150},
            'last_name': {'required': True, 'max_length': 150},
            'password': {'required': True, 'max_length': 150},
        }
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('username', 'email'),
                message=("Пользователь с указанными именем или адресом есть.")
            )
        ]

    def validate_username(self, value):
        if not name_is_valid(value):
            raise serializers.ValidationError('Содержит недопустимые символы.')
        if isinstance(value, str) and len(value) == 0:
            raise serializers.ValidationError('Имя указывать обязательно.')
        return value

    def validate_email(self, value):
        if isinstance(value, str) and len(value) == 0:
            raise serializers.ValidationError('e-mail указывать обязательно.')
        try:
            obj = self.Meta.model.objects.get(email=value)
        except self.Meta.model.DoesNotExist:
            return value
        if self.instance and obj.id == self.instance.id:
            return value
        else:
            raise serializers.ValidationError('Этот e-mail уже ииспользуется')


class UserMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role',)
        extra_kwargs = {
            'username': {'required': True, 'max_length': 150},
            'email': {'required': True, 'max_length': 254},
            'first_name': {'allow_blank': True, 'max_length': 150},
            'last_name': {'allow_blank': True, 'max_length': 150},
            'role': {'default': 'user'}
        }

    def validate_username(self, value):
        if not name_is_valid(value):
            raise serializers.ValidationError('Содержит недопустимые символы.')
        return value


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Значение не может быть me.')
        if not name_is_valid(value):
            raise serializers.ValidationError('Содержит недопустимые символы.')
        return value


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, allow_blank=False)
    confirmation_code = serializers.CharField(allow_blank=False)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Значение не может быть me.')
        if not name_is_valid(value):
            raise serializers.ValidationError('Содержит недопустимые символы.')
        return value
