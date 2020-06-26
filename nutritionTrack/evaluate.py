from dataclasses import dataclass

@dataclass
class Ingredient:
    Name: str
    Kalories: float #an 100 gramms
    Proteins: float
    Fat: float
    Carbohydrates: float

class Dish:
    Name:str = None
    Recipe = [] 
    TotalWeight: float = None
    Kalories:float = None #an 100 gramms
    Proteins:float = None
    Fat:float = None
    Carbohydrates:float = None

    def __str__(self):
        return f"Kalories = {self.Kalories:0.2f}, Proteins = {self.Proteins:0.2f}, Fat = {self.Fat:0.2f}, Carbohydrates = {self.Carbohydrates:0.2f}"

    def calc(self):
        if self.TotalWeight == 0:
            self.Kalories = 0
            self.Proteins = 0
            self.Fat = 0
            self.Carbohydrates = 0
            return 

        kalories = proteins = fat = carbohydrates = 0
        
        print(f"\n{'Name'.center(20)}|{'Kalories'.center(11)} | {'Proteins'.center(9)} | {'Fat'.center(9)} | {'Carbohydrates'.center(9)}\n{'-'*72}")
        for entry in self.Recipe:
            ingredient = entry[0]
            amount = entry[1]

            k = ingredient.Kalories * amount/100
            p = ingredient.Proteins * amount/100
            f = ingredient.Fat * amount/100
            c = ingredient.Carbohydrates * amount/100

            kalories += k
            proteins += p
            fat += f
            carbohydrates += c
            print(
f"{ingredient.Name.center(20)} \
{(str(round(k, 2))+'kkal.').center(11)}   \
{(str(round(p, 2))+'g.'   ).center(9)}   \
{(str(round(f, 2))+'g.'   ).center(9)}   \
{(str(round(c, 2))+'g.'   ).center(13)}")

        self.Kalories = kalories/(self.TotalWeight/100)
        self.Proteins = proteins/(self.TotalWeight/100)
        self.Fat = fat/(self.TotalWeight/100)
        self.Carbohydrates = carbohydrates/(self.TotalWeight/100)
        
        print(self.__str__())

    def __init__(self, Name, Recipe, TotalWeight = None):
        self.Name = Name
        self.Recipe = Recipe[:]

        if not TotalWeight:
            amount = 0
            for entry in self.Recipe:
                amount += entry[1]
            self.TotalWeight = amount
        else:
            self.TotalWeight = TotalWeight

def json_provided_format_decorator(func):

    def wrapper(json_input):
        name = 'None'
        recipe = []
        ingredient_items = json_input['food_items']
        for item in ingredient_items:
            recipe.append( (Ingredient(item['ingredient']['name'], 
                                        item['ingredient']['k'],
                                        item['ingredient']['p'],
                                        item['ingredient']['f'],
                                        item['ingredient']['c'],
                                        ), item['amount']) )
        amount = json_input['total_amount']
        return func(name, recipe, amount)
    return wrapper

@json_provided_format_decorator
def evaluate_ration(name, recipe, amount):

    eval_meal = Dish(name, recipe, amount)
    eval_meal.calc()

    result = {
        'kcals': eval_meal.Kalories,
        'carbs': eval_meal.Carbohydrates,
        'prots': eval_meal.Proteins,
        'fats': eval_meal.Fat,
    }
    return result


        
