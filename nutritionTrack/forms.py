from django import forms
from .models import Ingredient
import json

class FoodItemForm(forms.Form):
    amount = forms.DecimalField(
        min_value=0,
        widget = forms.NumberInput(attrs={}),
    )

class DateField(forms.MultiValueField):
    def __init__(self, **kwargs):
        fields = (
            forms.BooleanField(
                required=False,
            ),
            forms.DecimalField(
                required=False,
            ),
        )
        super().__init__(fields=fields, require_all_fields=False, **kwargs)

    def compress(self, data_list):
        return json.dumps(data_list, default=float)

class DateWidget(forms.MultiWidget):
    def __init__(self, *attrs, **kwargs):
        widgets = [forms.CheckboxInput(), forms.NumberInput(), ]
        super().__init__(widgets, *attrs, **kwargs)

    def decompress(self, value):
        if value == None:
            return [None, None]
        else:
            return value        

class DateForm(forms.Form):
    def __init__(self, date, mode, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if mode == 'Add':
            ingredients = Ingredient.objects.all()
            foodItems = []
            for item in ingredients:
                foodItems.append({'pk': item.pk, 'amount': 0,})
        if mode == 'Change':
            foodItems = date.ration
        self.foodItemsNames = dict()
        self.foodItemsPKs = dict()
        for dic in foodItems:
            field_name = 'foodItem_%s' % (dic['pk'], )
            self.fields[field_name] = DateField(required=False, widget=DateWidget())
            ingredient = Ingredient.objects.get(pk=dic['pk'])
            self.foodItemsNames[field_name] = ingredient.name
            self.foodItemsPKs[field_name] = dic['pk']

    def clean(self):
        foodItems = list()
        for i in self.foodItemsPKs.values():
            food_field = 'foodItem_%s' % (i, )
            pair = self.cleaned_data[food_field]
            pair = json.loads(pair)
            if pair[0] == True:
                foodItems.append({'pk': i, 'amount': pair[1]})
        self.cleaned_data['food_items'] = foodItems

    def get_food_item_fields(self):
        for field_name in self.fields:
            if field_name.startswith('foodItem_'):
                yield {'name': self.foodItemsNames[field_name],
                        'field': self[field_name],}

class IngredientField(forms.MultiValueField):
    def __init__(self, **kwargs):
        fields = (
            forms.BooleanField(
                required=False
            ),
            forms.DecimalField(
                required=False
            )
        )
        super().__init__(fields=fields, require_all_fields=False, **kwargs)

    def compress(self, data_list):
        return json.dumps(data_list, default=float)

class IngredientWidget(forms.MultiWidget):
    def __init__(self, *attrs, **kwargs):
        widgets = [forms.CheckboxInput(), forms.NumberInput(), ]
        super().__init__(widgets, *attrs, **kwargs)

    def decompress(self, value):
        if value == None:
            return [None, None]
        else:
            return value

class DishForm(forms.Form):
    name = forms.CharField(
        label='anylabel',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'enter a name',
        }))
    totalAmount = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "0",
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ingredients = Ingredient.objects.all()
        self.ingredientNames = dict()
        self.ingredientPKs = dict()
        for i in range(len(ingredients)):
            field_name = 'ingredient_%s' % (i, )
            self.fields[field_name] = IngredientField(required=False, widget=IngredientWidget())
            self.ingredientNames[field_name] = ingredients[i].name
            self.ingredientPKs[field_name] = ingredients[i].pk
    
    def clean(self):
        i = 0 
        ingredients = dict()
        ingredient = 'ingredient_%s' % (i, )
        while self.cleaned_data.get(ingredient):
            pair = json.loads(self.cleaned_data[ingredient])
            if pair[0] == True:
                ingredients[self.ingredientPKs[ingredient]] = pair[1]
            i += 1
            ingredient = 'ingredient_%s' % (i, )
        self.cleaned_data['ingredients'] = ingredients

    def get_ingredient_fields(self):
        for field_name in self.fields:
            if field_name.startswith('ingredient_'):
                yield {'name': self.ingredientNames[field_name],
                        'field': self[field_name]}

class IngredientForm(forms.Form):
    name = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'enter a name',
        }))
    kcals = forms.DecimalField(
        min_value=0,
        widget = forms.NumberInput(attrs={}),
    )
    carbs = forms.DecimalField(
        min_value=0,
        widget = forms.NumberInput(attrs={}),
    )
    prots = forms.DecimalField(
        min_value=0,
        widget = forms.NumberInput(attrs={}),
    )
    fats = forms.DecimalField(
        min_value=0,
        widget = forms.NumberInput(attrs={}),
    )

