from django.contrib import admin
from .models import Ingredient, Dish, Date

class IngredientAdmin(admin.ModelAdmin):
    pass

class DishAdmin(admin.ModelAdmin):
    pass

class DateAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Date, DateAdmin)
