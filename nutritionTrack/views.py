from django.shortcuts import render, redirect
from datetime import datetime
from .models import Date, Ingredient, Dish
from .evaluate import evaluate_ration
from .forms import DishForm, IngredientForm, DateForm, FoodItemForm
from django.contrib.auth.decorators import login_required
import json
from django.core.exceptions import ObjectDoesNotExist 

@login_required(redirect_field_name="")
def specific_date(request, the_date=None):
    
    #a main page providing main purpose support


    if the_date == None:
        the_date = datetime.date(datetime.now())
        return redirect('specific_date', the_date.strftime(r'%Y-%m-%d'))

    user = request.user

    if type(the_date) is str:
        the_date = datetime.fromisoformat(the_date)

    try :
        date = Date.objects.get(user=user, date=the_date)
    except Date.DoesNotExist:
        date = None

    if date == None:
        date = Date(date=the_date, user=user)
        date.save()
    
    ration = date.ration
    food_items = ration['food_items']

    foodItems = []
    food_list_eval = []
    total_amount = 0

    for item in food_items:
        try:
            ingredient = Ingredient.objects.get(pk=item['pk'])
        except ObjectDoesNotExist:
            ingredient = None
        if ingredient == None:
            date.ration['food_items'].remove(item)
            date.save()
            continue
        foodItems.append({'id':item['id'],
                        'name':ingredient.name, 
                        'amount':item['amount'], })
        total_amount += item['amount']

        food_list_eval.append({'ingredient':   {'name': 'None',
                                                'k': float(ingredient.kcals), 
                                                'p': float(ingredient.prots), 
                                                'f': float(ingredient.fats),
                                                'c': float(ingredient.carbs),},

                                    'amount':   item['amount'],       })

    kpfc = evaluate_ration({'food_items': food_list_eval, 'total_amount': None,})
    kpfc['kcals'] *= total_amount/100
    kpfc['carbs'] *= total_amount/100
    kpfc['prots'] *= total_amount/100
    kpfc['fats'] *= total_amount/100

    context = {
        'foodItems': foodItems,
        'kpfc': kpfc,
        'the_date': str(date.pk),
        'date_value': date.date.strftime(r'%Y-%m-%d'),
        'next_target': 'specific_date %s' % (the_date.strftime(r'%Y-%m-%d'), ),
    }

    return render(request, 'specific_date.html', context)

@login_required(redirect_field_name='')
def edit_date(request, func='None', date_pk='None', 
                food_id='None', next_target='None'):
    if func == 'None': # if func is None then it's meaningless to be here
        if next_target == 'None':
            response = redirect('actual_date')
            return response
        else:
            next_target = next_target.split()
            response = redirect(*next_target)
            return response    

    if date_pk == 'None':
        the_date = datetime.date(datetime.now())
        user = request.user
        try:
            date = Date.objects.get(user=user, date=the_date)
        except Date.DoesNotExist:
            date = Date()
            date.user = user
            date.save()
    else:
        date = Date.objects.get(pk=int(date_pk))

    if func == 'Del':
        if food_id == 'None':
            if next_target == 'None':
                return redirect('actual_date')
            else:
                next_target = next_target.split()
                return redirect(*next_target)

        date = Date.objects.get(pk=date_pk)
        ration = date.ration
        food_items = ration['food_items']
        food_items = [ item for item in food_items if item['id'] != int(food_id)]
        ration['food_items'] = food_items
        date.ration = ration
        date.save()

        if next_target == 'None':
            return redirect('actual_date')
        else:
            next_target = next_target.split()
            return redirect(*next_target)
    
    name = 'None'
    if func == 'Change':
        dateForm = FoodItemForm()
        for item in date.ration['food_items']:
            if item['id'] == int(food_id):
                ing_pk = item['pk']
                ing = Ingredient.objects.get(pk=ing_pk)
                name = ing.name
        if request.method == 'POST':
            dateForm = FoodItemForm(request.POST)
            if dateForm.is_valid():
                ration = date.ration
                food_items = ration['food_items']
                for item in food_items:
                    if item['id'] == int(food_id):
                        item['amount'] = float(dateForm.cleaned_data['amount'])
                ration['food_items'] = food_items
                date.ration = ration
                date.save()

                if next_target == 'None':
                    return redirect('actual_date')
                else:
                    next_target = next_target.split()
                    return redirect(*next_target)


    if func == 'Add':
        dateForm = DateForm(date, 'Add')
        if request.method == 'POST':
            dateForm = DateForm(date, 'Add', request.POST)
            if dateForm.is_valid():
                ration_add = dateForm.cleaned_data['food_items']
                ration = date.ration
                food_items = ration['food_items']
                food_items += ration_add
                
                for i in range(len(food_items)):
                    food_items[i]['id'] = i
                ration['food_items'] = food_items
                date.ration = ration
                date.save()

                if next_target == 'None':
                    return redirect('actual_date')
                else:
                    next_target = next_target.split()
                    return redirect(*next_target)

    context = {
        'form': dateForm,
        'func': func,
        'name': name, #if func == 'Change'
        'date_pk': date_pk,
        'next_target': next_target,
    }

    return render(request, 'date_edit.html', context)

@login_required(redirect_field_name="")
def dates_list(request):
    user = request.user
    dates = Date.objects.filter(user=user)
    context = {
        'dates': dates
    }
    return render(request, 'dates_list.html', context)

@login_required(redirect_field_name="")
def list_ingredient(request):
    ingredients = Ingredient.objects.all()
    for ingredient in ingredients:
        ingredient = {
            'pk': ingredient.pk,
            'name': ingredient.name,
            'kcals': ingredient.kcals,
            'carbs': ingredient.carbs,
            'prots': ingredient.prots,
            'fats': ingredient.fats,
       }

    context = {
        'ingredients': ingredients,
    }
    return render(request, 'ingredient_list.html', context)

@login_required(redirect_field_name="")
def edit_ingredient(request, func='None', pk='None', next_target='None'):
    if func == 'None': # if func is None then it's meaningless to be here
        if next_target == 'None':
            response = redirect('ingredient_list')
            return response
        else:
            response = redirect(next_target)
            return response
  

    ingredientForm = IngredientForm()
    ingredient = None
    
    if func == 'Del':
        ingredient = Ingredient.objects.get(pk=pk)
        ingredient.delete()
        if next_target == 'None':
            response = redirect('ingredient_list')
            return response
        else:
            response = redirect(next_target)
            return response


    if func == 'Change':
        ingredient = Ingredient.objects.get(pk=pk)
        if request.method == 'POST':
            ingredientForm = IngredientForm(request.POST)
            if ingredientForm.is_valid():
                ingredient = Ingredient.objects.get(pk=pk)
                ingredient.name = ingredientForm.cleaned_data['name']
                ingredient.kcals = ingredientForm.cleaned_data['kcals']
                ingredient.carbs = ingredientForm.cleaned_data['carbs']
                ingredient.prots = ingredientForm.cleaned_data['prots']
                ingredient.fats = ingredientForm.cleaned_data['fats']
                ingredient.save()
                if next_target == 'None':
                    response = redirect('ingredient_edit', 'None', pk, 'None')
                    return response
                else:
                    response = redirect(next_target)
                    return response

    if func == 'Add':
        if request.method == 'POST':
            ingredientForm = IngredientForm(request.POST)
            if ingredientForm.is_valid():
                ingredient = Ingredient()
                ingredient.name = ingredientForm.cleaned_data['name']
                ingredient.kcals = ingredientForm.cleaned_data['kcals']
                ingredient.carbs = ingredientForm.cleaned_data['carbs']
                ingredient.prots = ingredientForm.cleaned_data['prots']
                ingredient.fats = ingredientForm.cleaned_data['fats']
                ingredient.save()
                if next_target == 'None':
                    response = redirect('ingredient_edit', 'Change', ingredient.pk , 'None')
                    return response
                else:
                    response = redirect(next_target)
                    return response

    context = {
        'form': ingredientForm,
        'next_target': next_target,
        'pk': pk,
        'ingredient': ingredient,
        'func': func,
    }

    return render(request, 'ingredient_edit.html', context)
    
@login_required(redirect_field_name="")
def list_dish(request):
    dishes = Dish.objects.all()
    for dish in dishes:
        dish = {
            'pk': dish.pk,
            'name': dish.name,
            'totalAmount': dish.totalAmount,
            'ingredients': dish.ingredients,
       }

    context = {
        'dishes': dishes,
    }
    return render(request, 'dish_list.html', context)

@login_required(redirect_field_name="")
def edit_dish(request, func='None', pk='None', next_target='None'):
    if func == 'None': # if func is None then it's meaningless to be here
        if next_target == 'None':
            response = redirect('dish_list')
            return response
        else:
            response = redirect(next_target)
            return response
  

    dishForm = DishForm()
    dish = None
    
    if func == 'Del':
        dish = Dish.objects.get(pk=pk)
        dish.delete()
        if next_target == 'None':
            response = redirect('dish_list')
            return response
        else:
            response = redirect(next_target)
            return response


    if func == 'Change':
        if request.method == 'POST':
            dishForm = DishForm(request.POST)
            if dishForm.is_valid():
                dish = Dish.objects.get(pk=pk)
                dish.name = dishForm.cleaned_data['name']
                dish.totalAmount = dishForm.cleaned_data['totalAmount']

                ingredients = dishForm.cleaned_data['ingredients']
                dish.ingredients = json.dumps(ingredients)

                food_list_eval = []
                for pk, amount in ingredients.items():
                    ingredient = Ingredient.objects.get(pk=pk)
                    food_list_eval.append({'ingredient':   {'name': ingredient.name,
                                                            'k': float(ingredient.kcals), 
                                                            'p': float(ingredient.prots), 
                                                            'f': float(ingredient.fats),
                                                            'c': float(ingredient.carbs),},

                                            'amount':       amount, })

                ingredient = dish.refIngredient
                if ingredient == None:
                    ingredient = Ingredient()
                    dish.refIngredient = ingredient
                ingredient.name = dish.name
                kpfc = evaluate_ration({'food_items': food_list_eval, 'total_amount': dish.totalAmount,})
                ingredient.kcals = kpfc['kcals']
                ingredient.carbs = kpfc['carbs']
                ingredient.prots = kpfc['prots']
                ingredient.fats = kpfc['fats']
                ingredient.save()

                dish.save()
                if next_target == 'None':
                    response = redirect('dish_list')
                    return response
                else:
                    response = redirect(next_target)
                    return response

    if func == 'Add':
        if request.method == 'POST':
            dishForm = DishForm(request.POST)
            if dishForm.is_valid():
                dish = Dish()
                dish.name = dishForm.cleaned_data['name']
                dish.totalAmount = dishForm.cleaned_data['totalAmount']
                
                ingredients = dishForm.cleaned_data['ingredients']
                dish.ingredients = json.dumps(ingredients)

                food_list_eval = []
                for pk, amount in ingredients.items():
                    ingredient = Ingredient.objects.get(pk=pk)
                    food_list_eval.append({'ingredient':   {'name': ingredient.name,
                                                            'k': float(ingredient.kcals), 
                                                            'p': float(ingredient.prots), 
                                                            'f': float(ingredient.fats),
                                                            'c': float(ingredient.carbs),},

                                            'amount':       amount, })


                ingredient = Ingredient()
                ingredient.name = dish.name
                kpfc = evaluate_ration({'food_items': food_list_eval, 'total_amount': dish.totalAmount,})
                ingredient.kcals = kpfc['kcals']
                ingredient.carbs = kpfc['carbs']
                ingredient.prots = kpfc['prots']
                ingredient.fats = kpfc['fats']
                ingredient.save()

                dish.refIngredient = ingredient
                dish.save()

                if next_target == 'None':
                    response = redirect('dish_list')
                    return response
                else:
                    response = redirect(next_target)
                    return response

    context = {
        'form': dishForm,
        'next_target': next_target,
        'pk': pk,
        'dish': dish,
        'func': func,
    }

    return render(request, 'dish_edit.html', context)