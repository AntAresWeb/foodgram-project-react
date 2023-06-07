from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, blank=True)
    slug = models.SlugField(max_length=200, blank=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)
