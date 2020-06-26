# Merva
Food values Calculations

Please follow the following steps to install project:
1. Clone this repo from your working directory using: git clone https://github.com/MikhailTselousov/Merva.git
2. Create venv
3. Activate venv
4. Install django using: pip install Django
5. Instal django json field using: pip install django-jsonfield
6. Create Djnago super user from manage.py using: python3 manage.py createsuperuser
7. Run server from manage.py using: python3 manage.py runserver
8. Try the web app by localhost:8000

if you want email features configure the email settings in settings.py

Usage guide:

The first page you will is 'sign up' page. 
Use its form to registrate yourself up. 
Email field is optionally for password resetting.

If you have already have account. 
Use login link from navbar to login or use link http://localhost:8000/accounts/login/

After you've logged in you will be redirected to actual date page. 
This page represents your ration for a today. 
You can here add some food using "add one" button belowe.

Initially there is no any food to add to your ration. 
So go to ingrediet list page using corresponding link button from nav bar or use link 
  http://localhost:8000/nutrition-track/ingredient_list/
Then press "add one" button and fill up form with approprite values.
  (WARNING: please use only approprite values for fields bacouse properly property validations has not been added yet, 
    for example: str format for 'name' field and float format with dots (not commas) for next fields. Otherwise result is unespectefull).
Then you will be redirected back to ingredient list. And now you can use editing and removing features for your ingredient.

Now you can add food to your ration. Go to the page using "Today date" link button from nav bar. Then press 'add one' button.
  In revealed page use input field to input amount of such ingredient. And press "add".
  Then you can change amount of your ingredient or delete it from today ration page.
 
If you want to add your own dish from some recipe. Use 'dish list' link button from nav bar. And then press 'add one'.
Fill up following fields: name, total amount, and tick wanted ingredients with fillig up amount of its. Then press save.
Then you will be redirected to 'ingredient list'. 
You can also edit or remove dish from 'dish list' page.

Also you can change or reset the password using appropriate link buttons from nav bar.

    
