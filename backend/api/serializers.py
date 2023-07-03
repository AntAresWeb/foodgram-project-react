import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from essences.models import Content, Ingredient, Recipe, Tag
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


class ContetnSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='igredient.id')
    name = serializers.CharField(source='igredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='igredient.measurement_unit', read_only=True)

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


class RecipeSerializer(serializers.ModelSerializer):
#    tags = TagSerialiser(source='id', many=True)
    tags = serializers.ListField(child=TagSerialiser())
    author = UserListSerializer(many=False, read_only=True)
    ingredients = ContetnSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

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
        contents = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.author = self.request.user
        recipe.save()
        for content in contents:
            ingredient = Content.objects.get_or_create(
                ingredient=content['id'], recipe=recipe)
            ingredient.amount += content['amount']
            ingredient.save()
        return recipe


class TestSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.IntegerField())
#    tags = serializers.ListField(child=TagSerialiser())
#    tags = TagSerialiser(many=True, read_only=True)
    
    class Meta:
        model = Recipe
        fields = ('id', 'tags', )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.first()
        for tag in tags:
            print(tag)
            #tag = get_object_or_404(Tag, id=tag)
            #recipe.add()
        return recipe
