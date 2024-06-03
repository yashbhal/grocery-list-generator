import unittest
import json
from unittest.mock import patch
from main import load_recipe_list, get_ingredients, print_recipes, validate_integer_input, validate_choice

class TestRecipeFunctions(unittest.TestCase):

    def setUp(self):
        self.recipes = [
            {
                "title": "Recipe 1",
                "number": 1,
                "ingredients": ["ingredient1, ingredient2"]
            },
            {
                "title": "Recipe 2",
                "number": 2,
                "ingedients": ["ingredient1, ingredient3, ingredient4"]
            },
            {
                "title": "Recipe 3",
                "number": 3,
                "ingedients": ["ingredient1, ingredient3, ingredient4", "ingredient5"]
            }
        ]

    def test_load_recipe_list(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data=json.dumps({"recipes": self.recipes}))) as mock_file:
            recipes_list = load_recipe_list('fake_path')
            self.assertEqual(recipes_list, self.recipes)
            mock_file.assert_called_with('fake_path')      


    def test_get_ingredients(self):
        ingredients = get_ingredients(1, self.recipes)
        self.assertEqual(ingredients, ["ingredient1, ingredient2"])
        ingredients = get_ingredients(4, self.recipes)
        self.assertEqual(ingredients, [])


    def test_print_recipes(self):
        output = print_recipes(self.recipes)
        expected_output = '\nRecipe Menu\n\n1. Recipe 1\n2. Recipe 2\n3. Recipe 3\n'
        self.assertEqual(output.strip(), expected_output.strip())    


    @patch('builtins.input', side_effect=['a', '2'])
    def test_validate_integer_input(self, mock_input):
        with patch('builtins.print') as mock_print:
            with self.assertRaises(ValueError) as context:
                validate_integer_input("Enter an integer: ")
            self.assertEqual(str(context.exception), "Invalid input. Enter a valid integer.")
            result = validate_integer_input("Enter an integer: ")
            self.assertEqual(result, 2)
            self.assertEqual(mock_input.call_count, 2)


    @patch('main.validate_integer_input', side_effect=[5])
    def test_valid_choice(self, mock_validate_integer_input):
        max_value = 10
        result = validate_choice("Enter a number: ", max_value)
        self.assertEqual(result, 5)
        mock_validate_integer_input.assert_called_once_with("Enter a number: ")


    @patch('main.validate_integer_input', side_effect=[15])
    def test_invalid_choice_above_max(self, mock_validate_integer_input):
        max_value = 10
        with self.assertRaises(ValueError) as context:
            validate_choice("Enter a number: ", max_value)
        self.assertEqual(str(context.exception), "Invalid recipe choice. Enter a number between 1 and 10")
        mock_validate_integer_input.assert_called_once_with("Enter a number: ")


    @patch('main.validate_integer_input', side_effect=[-1])
    def test_invalid_choice_below_min(self, mock_validate_integer_input):
        max_value = 10
        with self.assertRaises(ValueError) as context:
            validate_choice("Enter a number: ", max_value)
        self.assertEqual(str(context.exception), "Invalid recipe choice. Enter a number between 1 and 10")
        mock_validate_integer_input.assert_called_once_with("Enter a number: ")


if __name__ == '__main__':
    unittest.main()