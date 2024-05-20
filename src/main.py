import json

def load_recipe_list():
    with open('recipes.json') as recipe_file:
        recipe_list = json.load(recipe_file)
    return recipe_list['recipes']


def get_ingredients(recipe_title, recipes_list):
    for recipe in load_recipe_list():
        if recipe.get('title') == recipe_title:
            return recipe.get('ingredients')


def print_recipes(recipes_list):
    print('\nWhich one of the following recipes would you like to eat this week?: \n')
    for recipe in recipes_list:
        print(recipe.get('title'))


def main():
    recipes_list = load_recipe_list()
    print_recipes(recipes_list)
    recipe_choice = input("Enter the name of the recipe you want to cook: ")
    ingredients = get_ingredients(recipe_choice, recipes_list)
    print(ingredients)


if __name__ == "__main__":
    main()