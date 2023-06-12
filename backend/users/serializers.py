from rest_framework import serializers

from essences.models import Subscribe
from users.models import User
from .utils import name_is_valid


class UserListSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed',)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated is True:
            return user.subscriber.filter(author=obj).exists()
        else:
            return False


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password',)
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }


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
