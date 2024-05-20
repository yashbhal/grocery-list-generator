import json

def load_read_recipe_list():
    with open('recipes.json') as recipe_file:
        parsed_recipe_list = json.load(recipe_file)
    return parsed_recipe_list