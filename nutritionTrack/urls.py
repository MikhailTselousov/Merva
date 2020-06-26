from django.urls import path, register_converter
from nutritionTrack import views, converters

register_converter(converters.YearMonthDayConverter, 'yyyy-mm-dd')

urlpatterns = [
    path("", views.specific_date, name='actual_date'),
    path("<yyyy-mm-dd:the_date>/", views.specific_date, name='specific_date'),
    path("date_edit/<func>/<date_pk>/<food_id>/<next_target>/", views.edit_date, name="date_edit"),

    path("ingredient_list/", views.list_ingredient, name='ingredient_list'),
    path("ingredient_edit/<func>/<pk>/<next_target>/", views.edit_ingredient, name="ingredient_edit"),

    path("dish_list/", views.list_dish, name='dish_list'),
    path("dish_edit/<func>/<pk>/<next_target>/", views.edit_dish, name="dish_edit"),

    path("dates_list/", views.dates_list, name="dates_list"),

]