from django_filters.rest_framework import FilterSet

from essences.models import Ingredient


class IngredientFilter(FilterSet):
    class Meta:
        model = Ingredient
        fields = {
            'name': ['startswith'],
        }
        together = ('name',)
