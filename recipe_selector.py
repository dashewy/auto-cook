import json
import yaml
import random

def get_json_recipes(file):
    with open(file, 'r') as f:
        recipes = json.load(f)

    return recipes

def get_yaml_recipes(file):
    with open(file, 'r') as f:
        recipes = yaml.safe_load(f)

    return recipes

def get_ingredients(recipes ,meal, dish):
    # get all k, v ingredients, and return dish for output txt
    return recipes[meal][dish], dish

def combine_ingredients(ingredients, extra_ingredients):
    # get ingredients then add if already in grocery list
    if not ingredients:
        return extra_ingredients
    
    merge = ingredients | extra_ingredients
    all_keys = list(merge.keys())
    return {k: ingredients.get(k, 0) + extra_ingredients.get(k, 0) for k in all_keys}

def food_format(food_dict):
    # stringify list of dicts
    return [f"{v} {k.replace('_', ' ')}" for k, v in food_dict.items()]

def rand_meals(recipes, meal, num): 
    meals = list(recipes[meal].keys())
    # random.sample is unique (without replacement)
    return random.sample(meals, k=num)

def rand_run(rec, ml):
    match ml:
        case 'breakfast':
            # default to 1 if not found
            num = rec.get('num_breakfast', 1)
        case 'lunch':
            # default to 2 if not found
            num = rec.get('num_lunch', 2)
        case 'dinner':
            # default to 3 if not found
            num = rec.get('num_dinner', 3)

    all_ings = {}
    meals = ''
    dishes = rand_meals(rec, ml, num)
    for dish in dishes:
        ing, mls = get_ingredients(rec, ml, dish)
        all_ings = combine_ingredients(all_ings, ing)
        meals += mls + ' '

    return all_ings, meals

def rand_handler(file_type):
   # picks meals and randoms and combines ingredients + tells you menu
   match file_type:
       case 'json':
           recipes = get_json_recipes('recipes.json')
       case 'yaml':
           recipes = get_yaml_recipes('recipes.yaml')

   meal_types = frozenset(['breakfast', 'lunch', 'dinner'])
   ingredients = {}
   all_meals = ''

   for meal in meal_types:
       ings, mls = rand_run(recipes, meal)
       ingredients.update(ings)
       all_meals += mls

   split_meals = all_meals.strip().split(' ')
   list_of_meals = [ml.replace('_', ' ') for ml in split_meals]

   # shortcuts expects a dictionary     
   rand_dict = {'ingredients': food_format(ingredients), 'meals': list_of_meals}
   return rand_dict

def meal_handler(file_type, dishes):
    if not isinstance(dishes, list):
        dishes = list(dishes)
    # takes list of meals and returns combined ingredients
    clean_dishes = [dish.strip().lower() for dish in dishes]
    meal_types = frozenset(['breakfast', 'lunch', 'dinner'])
    all_dishes = {}
    all_ingredients = {}
    
    match file_type:
        case 'json':
            recipes = get_json_recipes('recipes.json')
        case 'yaml':
            recipes = get_yaml_recipes('recipes.yaml')
            clean_dishes = [dish.replace(' ', '_') for dish in clean_dishes]    

    for ml in meal_types:
        all_dishes.update(recipes.get(ml))
        
    for dish in clean_dishes:
        all_ingredients = combine_ingredients(all_ingredients, all_dishes.get(dish, {}))
    
    # shortcuts ecpects a dictionary 
    ing_dict = {'ingredients': food_format(all_ingredients)}
    return ing_dict
    

if __name__ == '__main__':
    # shortcut expects a list
    pass
    # rand_test = rand_handler('yaml')
    # print(rand_test)

    # meal_test = meal_handler('yaml', ['Meatloaf', 'Eggs on toast', 'Sandwich', 'Spaghetti'])
    # print(f'meal test: {meal_test}')
