from django.db import models
from django.conf import settings
import jsonfield

class Ingredient(models.Model):
    name = models.CharField(max_length=20)
    kcals = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)
    prots = models.DecimalField(max_digits=5, decimal_places=2)
    fats = models.DecimalField(max_digits=5, decimal_places=2)

class Dish(models.Model):
    name = models.CharField(max_length=20)
    totalAmount = models.PositiveSmallIntegerField()
    ingredients = jsonfield.JSONField()
    refIngredient = models.ForeignKey('Ingredient', on_delete=models.SET_NULL, null=True, default=None)


class Date(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ration = jsonfield.JSONField(default={'food_items': []})