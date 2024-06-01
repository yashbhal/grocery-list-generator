import unittest
import json
from unittest.mock import patch
from main import load_recipe_list

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

if __name__ == '__main__':
    unittest.main()