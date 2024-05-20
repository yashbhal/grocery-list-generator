import json

def load_recipe_list():
    with open('recipes.json') as recipe_file:
        recipe_list = json.load(recipe_file)
    return recipe_list['recipes']


def get_ingredients(recipe_title):
    for recipe in load_recipe_list():
        if recipe.get('title') == recipe_title:
            return recipe.get('ingredients')


