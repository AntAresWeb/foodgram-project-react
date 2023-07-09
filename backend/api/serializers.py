import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from essences.models import Content, Ingredient, Recipe, Tag, User
from users.serializers import UserListSerializer


class IngredientSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
        read_only_fields = ('name', 'color', 'slug',)


class Contetn_Serializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = Content
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class ContetnSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = Content
        fields = ('id', 'name', 'measurement_unit', 'amount',)

    def to_internal_value(self, data):
        id = data.get('id')
        amount = data.get('amount')
        if not id:
            raise serializers.ValidationError(
                {'id': f'Это поле обязательно. Строка: {data}'}
            )
        if not amount:
            raise serializers.ValidationError(
                {'amount': f'Это поле обязательно. Строка: {data}'}
            )

        return {
            'id': id,
            'amount': amount,
        }


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class CurrentUserDefault:
    requires_context = False

    def __call__(self, serializer_field):
        return User.objects.get(id=1)
#        return serializer_field.context['request'].user


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerialiser(many=True)
    author = UserListSerializer(many=False)
    ingredients = ContetnSerializer(many=True, source='contents')
    is_favorited = serializers.SerializerMethodField(required=False)
    is_in_shopping_cart = serializers.SerializerMethodField(required=False)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time',)

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False


class RecipeWriteSerializer(serializers.ModelSerializer):
    ingredients = ContetnSerializer(many=True, source='contents')
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    author = UserListSerializer(many=False, default=CurrentUserDefault)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'ingredients', 'name', 'text',
                  'cooking_time', 'image')
        validators = (
            UniqueTogetherValidator(
                queryset=Ingredient.objects.all(),
                fields=('ingredients', )
            ),
        )

    def create(self, validated_data):
        contents = validated_data.pop('contents')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.add(*tags)

        for content in contents:
            recipe.ingredients.add(
                content.get('id'),
                through_defaults={'amount': content.get('amount')}
            )
        return recipe

    def update(self, instance, validated_data):
        contents = validated_data.pop('contents')

        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.add(*tags)

        instance.ingredients.clear()
        for content in contents:
            instance.ingredients.add(
                content.get('id'),
                through_defaults={'amount': content.get('amount')}
            )

        instance.save()
        return instance

    def validate_ingredients(self, value):
        ids = [content.get('id') for content in value]
        dup_ids = [x for i, x in enumerate(ids) if i != ids.index(x)]
        if len(dup_ids) > 0:
            raise serializers.ValidationError(
                f'В списке ингредиентов есть дубликаты c id = {dup_ids}'
            )
        not_ids = list(set(ids) - set(
            Ingredient.objects.all().values_list('id', flat=True))
        )
        if len(not_ids):
            raise serializers.ValidationError(
                f'В базе нет ингредиентов с id = {not_ids}'
            )
        return value
