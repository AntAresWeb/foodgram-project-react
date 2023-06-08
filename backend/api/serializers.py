from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from essences.models import Ingredient


class IngredientSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
