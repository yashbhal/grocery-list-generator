import json

def load_recipe_list():
    with open('recipes.json') as recipe_file:
        recipe_list = json.load(recipe_file)
    return recipe_list['recipes']


def get_ingredients(recipe_number, recipes_list):
    for recipe in load_recipe_list():
        if recipe.get('number') == recipe_number:
            return recipe.get('ingredients')


def print_recipes(recipes_list):
    print('\nWhich one of the following recipes would you like to eat this week?: \n')
    for recipe in recipes_list:
        print(recipe.get('title'))


def main():
    counter = 0
    recipes_list = load_recipe_list()
    print_recipes(recipes_list)
    recipe_amount = int(input("How many recipes would you like to prep for the week? "))
    while(counter<recipe_amount):
        recipe_choice = input("Enter the number of the recipe you want to cook: ")
        ingredients = get_ingredients(recipe_choice, recipes_list)
        print(ingredients)
        counter+=1


if __name__ == "__main__":
    main()