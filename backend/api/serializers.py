from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from essences.models import Ingredient, Tag


class IngredientSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
