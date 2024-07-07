import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton,
    QListWidget, QMessageBox, QDialog, QLineEdit, QHBoxLayout, QFormLayout
)
from PyQt6.QtCore import Qt

# Import functions from main.py
from main import load_recipe_list, get_ingredients, get_weeks_ingredients

class RecipeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = 'recipes.json'
        self.recipes_list = load_recipe_list(self.file_path)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Grocery List Generator')

        self.layout = QVBoxLayout()
        
        # Display available recipes
        self.recipes_label = QLabel('Available Recipes:')
        self.layout.addWidget(self.recipes_label)

        self.recipes_list_widget = QListWidget()
        self.load_recipes()
        self.layout.addWidget(self.recipes_list_widget)
        
        # Add, Edit, Remove buttons
        self.button_layout = QHBoxLayout()
        
        self.add_button = QPushButton('Add Recipe')
        self.add_button.clicked.connect(self.add_recipe)
        self.button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton('Edit Recipe')
        self.edit_button.clicked.connect(self.edit_recipe)
        self.button_layout.addWidget(self.edit_button)

        self.remove_button = QPushButton('Remove Recipe')
        self.remove_button.clicked.connect(self.remove_recipe)
        self.button_layout.addWidget(self.remove_button)
        
        self.layout.addLayout(self.button_layout)

        # Ask for the number of recipes
        self.num_recipes_label = QLabel('How many recipes would you like to prep for the week?')
        self.layout.addWidget(self.num_recipes_label)
        
        self.num_recipes_spinbox = QSpinBox()
        self.num_recipes_spinbox.setRange(1, len(self.recipes_list))
        self.layout.addWidget(self.num_recipes_spinbox)

        # Button to proceed with recipe selection
        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.show_recipe_selection_dialog)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)
    
    def load_recipes(self):
        self.recipes_list_widget.clear()
        for recipe in self.recipes_list:
            self.recipes_list_widget.addItem(f"{recipe['number']}. {recipe['title']}")
    
    def add_recipe(self):
        dialog = RecipeDialog(self)
        if dialog.exec():
            new_recipe = dialog.get_recipe_data()
            new_recipe['number'] = max(recipe['number'] for recipe in self.recipes_list) + 1
            self.recipes_list.append(new_recipe)
            self.save_recipes()
            self.load_recipes()
    
    def edit_recipe(self):
        selected_item = self.recipes_list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, 'Select Recipe', 'Please select a recipe to edit.')
            return

        selected_recipe_number = int(selected_item.text().split('.')[0])
        selected_recipe = next(recipe for recipe in self.recipes_list if recipe['number'] == selected_recipe_number)
        
        dialog = RecipeDialog(self, selected_recipe)
        if dialog.exec():
            updated_recipe = dialog.get_recipe_data()
            selected_recipe.update(updated_recipe)
            self.save_recipes()
            self.load_recipes()
    
    def remove_recipe(self):
        selected_item = self.recipes_list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, 'Select Recipe', 'Please select a recipe to remove.')
            return

        selected_recipe_number = int(selected_item.text().split('.')[0])
        self.recipes_list = [recipe for recipe in self.recipes_list if recipe['number'] != selected_recipe_number]
        self.save_recipes()
        self.load_recipes()
    
    def save_recipes(self):
        with open(self.file_path, 'w') as file:
            json.dump({'recipes': self.recipes_list}, file, indent=4)
    
    def show_recipe_selection_dialog(self):
        num_recipes = self.num_recipes_spinbox.value()
        dialog = RecipeSelectionDialog(num_recipes, self.recipes_list, self)
        dialog.exec()

class RecipeSelectionDialog(QDialog):
    def __init__(self, num_recipes, recipes_list, parent=None):
        super().__init__(parent)
        self.num_recipes = num_recipes
        self.recipes_list = recipes_list
        self.selected_recipes = []
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Select Recipes')
        self.layout = QVBoxLayout()
        
        self.instructions = QLabel(f'Select {self.num_recipes} recipes:')
        self.layout.addWidget(self.instructions)
        
        self.recipes_list_widget = QListWidget()
        self.recipes_list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for recipe in self.recipes_list:
            self.recipes_list_widget.addItem(f"{recipe['number']}. {recipe['title']}")
        self.layout.addWidget(self.recipes_list_widget)

        self.done_button = QPushButton('Done')
        self.done_button.clicked.connect(self.collect_selected_recipes)
        self.layout.addWidget(self.done_button)

        self.setLayout(self.layout)
    
    def collect_selected_recipes(self):
        selected_items = self.recipes_list_widget.selectedItems()
        if len(selected_items) != self.num_recipes:
            QMessageBox.warning(self, 'Invalid Selection', f'Please select exactly {self.num_recipes} recipes.')
            return
        
        for item in selected_items:
            recipe_number = int(item.text().split('.')[0])
            self.selected_recipes.append(recipe_number)
        
        self.show_ingredients()
    
    def show_ingredients(self):
        weeks_ingredients = get_weeks_ingredients(self.selected_recipes, self.recipes_list)
        
        ingredients_list = '\n'.join(f"- {ingredient}" for ingredient in weeks_ingredients)
        QMessageBox.information(self, 'Ingredients for the Week', f"The ingredients you need are:\n{ingredients_list}")
        
        self.accept()

class RecipeDialog(QDialog):
    def __init__(self, parent=None, recipe=None):
        super().__init__(parent)
        self.recipe = recipe or {'title': '', 'ingredients': []}
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Recipe Details')
        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()

        self.title_edit = QLineEdit(self.recipe['title'])
        self.form_layout.addRow('Title:', self.title_edit)

        self.ingredients_edit = QLineEdit(', '.join(self.recipe['ingredients']))
        self.form_layout.addRow('Ingredients (comma separated):', self.ingredients_edit)

        self.layout.addLayout(self.form_layout)
        
        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
    
    def get_recipe_data(self):
        title = self.title_edit.text()
        ingredients = [ingredient.strip() for ingredient in self.ingredients_edit.text().split(',')]
        return {'title': title, 'ingredients': ingredients}

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RecipeApp()
    window.show()
    sys.exit(app.exec())
