import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

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

    def to_internal_value(self, data):
        try:
            try:
                return Tag.objects.get(id=data)
            except KeyError:
                raise serializers.ValidationError('Нет тэга с таким id.')
            except ValueError:
                raise serializers.ValidationError(
                    'id тэга должен быть целым числом.')
        except Tag.DoesNotExist:
            raise serializers.ValidationError(
                'Не найден тэг с указанным id.')


class ContetnSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.IntegerField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = Content
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class CurrentUserDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerialiser(many=True)
    author = UserListSerializer(many=False, default=CurrentUserDefault)
    ingredients = ContetnSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(required=False)
    is_in_shopping_cart = serializers.SerializerMethodField(required=False)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        field = ('id', 'tags', 'author', 'ingredients',
                 'is_favorited', 'is_in_shopping_cart', 'name',
                 'image', 'text', 'cooking_time',)

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.author = self.context['request'].user
        for tag in tags:
            tag = get_object_or_404(Tag, id=tag)
            recipe.tags.add(tag)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)
        instance.save()
        return instance


class TestSerializer(serializers.ModelSerializer):
    ingredients = ContetnSerializer(many=True)
    tags = TagSerialiser(many=True)
    author = UserListSerializer(many=False, default=User.objects.get(id=1))
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'ingredients', 'name', 'text',
                  'cooking_time', 'image')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        print('-->>', ingredients)

        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.add(*tags)

        for ingredient in ingredients:
            amount = {'amount': ingredient.pop('amount')}
            id = ingredient.pop('ingredient').get('id')
            print('amount -->>', amount)
            print('id -->>', id)
            recipe.ingredients.add(Ingredient.objects.get(id=id), through_defaults=amount)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.contents.all().delete()
        for ingredient in ingredients:
            content, result = Content.objects.get_or_create(
                ingredient=ingredient,
                recipe=instance)
            if result:
                content.amount += ingredient['amount']
                content.save()
        instance.save()
        return instance
