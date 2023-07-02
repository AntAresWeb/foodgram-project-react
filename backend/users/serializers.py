from rest_framework import serializers

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
            return user.subscribes.filter(author=obj).exists()
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

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)

    class Meta:
        fields = ('new_password', 'current_password',)


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=254)

    class Meta:
        fields = ('password', 'email',)
