from recipe_selector import meal_handler
import sys
import json

if __name__ == '__main__':
    try: 
        foods = json.loads(sys.argv[1])
        # shortcuts sends dictionary
        food_list = foods.get('meals', [])
        print(json.dumps(meal_handler('yaml', food_list)))
    except:
        print('bad data')
