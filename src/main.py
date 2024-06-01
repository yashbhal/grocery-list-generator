import json

def load_recipe_list(file_path = 'recipes.json'):
    with open(file_path) as recipe_file:
        recipe_list = json.load(recipe_file)
    return recipe_list['recipes']


def get_ingredients(recipe_number, recipes_list):
    for recipe in recipes_list:
        if recipe.get('number') == recipe_number:
            return recipe.get('ingredients')
    return []


def print_recipes(recipes_list):
    output = '\nRecipe menu\n'
    for recipe in recipes_list:
        output += f"\n{ + recipe.get('number')}. {recipe.get('title')}"
    print(output)
    return output
    

def validate_integer_input(prompt):
    try:
        value = int(input(prompt))
        return value
    except ValueError:
        raise ValueError("Invalid input. Enter a valid integer.")


def validate_choice(prompt, max_value):
    value = validate_integer_input(prompt)
    if 1 <= value <= max_value:
        return value
    else:
        raise ValueError(f"Invalid recipe choice. Enter a number between 1 and {max_value}")


def get_weeks_ingredients(recipe_choices, recipes_list):
    weeks_ingredients = set()
    for recipe_choice in recipe_choices:        
        ingredients = get_ingredients(recipe_choice, recipes_list)
        if ingredients:
            weeks_ingredients.update(get_ingredients(recipe_choice, recipes_list))
        else:
            raise ValueError(f"No ingredients found for {recipe_choice}.")
    return list(weeks_ingredients)


def main():
    recipes_list = load_recipe_list()
    print_recipes(recipes_list)
    recipe_amount = validate_choice("How many recipes would you like to prep for the week? ", len(recipes_list))
    recipe_choices = []

    for _ in range(recipe_amount):
        recipe_choice = validate_choice("Enter the number of the recipe you want to cook: ", len(recipes_list))
        recipe_choices.append(recipe_choice)
    try:
        weeks_ingredients = get_weeks_ingredients(recipe_choices, recipes_list)
        print("\nIngredients for the week:")
        for ingredient in weeks_ingredients:
            print(f"- {ingredient}")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()