import json

def load_recipe_list():
    with open('recipes.json') as recipe_file:
        recipe_list = json.load(recipe_file)
    return recipe_list['recipes']


def get_ingredients(recipe_number, recipes_list):
    for recipe in load_recipe_list():
        if recipe.get('number') == recipe_number:
            return recipe.get('ingredients')
    return []


def print_recipes(recipes_list):
    print('\nRecipe menu\n')
    for recipe in recipes_list:
        print(f"{recipe.get('number')}. {recipe.get('title')}")
    

def validate_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Enter a valid integer.")


def validate_choice(prompt, max_value):
    while True:
        value = validate_integer_input(prompt)
        if 1 <= value <= max_value:
            return value
        else:
            print(f"Invalid recipe choice. Enter a number between 1 and {max_value}")


def main():
    counter = 0
    weeks_ingredients = set()
    recipes_list = load_recipe_list()
    print_recipes(recipes_list)
    recipe_amount = validate_choice("How many recipes would you like to prep for the week? ", len(recipes_list))

    while(counter < recipe_amount):
        recipe_choice = validate_choice("Enter the number of the recipe you want to cook: ", len(recipes_list))
        ingredients = get_ingredients(recipe_choice, recipes_list)
        if ingredients:
            weeks_ingredients.update(get_ingredients(recipe_choice, recipes_list))
        else:
            print(f"No ingredients found for {recipe_choice}.")
        counter+=1

    ingredients_list = list(weeks_ingredients)
    print(ingredients_list)


if __name__ == "__main__":
    main()