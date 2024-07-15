#Define Recipe class
class Recipe:
    #Variable to store all ingredients
    all_ingredients = set()

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = ""

    #Getter and Setter for name
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name

    #Getter and Setter for cooking_time
    def get_cooking_time(self):
        return self.cooking_time
    
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    #Adding a variable number of ingredients
    def add_ingredients(self, *ingredients):
        self.ingredients.extend(ingredients)
        self.update_all_ingredients()

    #Getter for ingredients
    def get_ingredients(self):
        for ingredient in self.ingredients:
            print("-" + str(ingredient))

    #Difficulty calculation
    def calculate_difficulty(self, cooking_time, ingredients):
        if cooking_time < 10:
            if len(ingredients) < 4:
                difficulty = "Easy"
            elif len(ingredients) >= 4:
                difficulty = "Medium"
        elif cooking_time >= 10:
            if len(ingredients) < 4:
                difficulty = "Intermediate"
            elif len(ingredients) >= 4:
                difficulty = "Hard"
        return difficulty

    #Getter for difficulty
    def get_difficulty(self):
        difficulty = self.calculate_difficulty(self.cooking_time, self.ingredients)
        output = "Difficulty: " + str(self.cooking_time)
        self.difficulty = difficulty
        return output
    
    #Ingredient Search
    def search_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            return True
        else:
            return False
        
    #Checks for ingredients in the list an then updates the ingredient list
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in self.all_ingredients:
                self.all_ingredients.add(ingredient)

    #Prints the recipe with formatting
    def __str__(self):
        output = (
            "Name: " + self.name
            + "\nCooking Time(min): " + str(self.cooking_time)
            + "\nIngredients: " + str(self.ingredients)
            + "\nDifficulty: " + str(self.difficulty) + "\n"
        )
        return output

#Searches a recipe based on a specific ingredient
    #data takes the recipe list
    #search_term takes the ingredient
def recipe_search(data, search_term):
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)

#Main Code

#Recipe setup
print("--------------------")
print("\nList of all Recipes: \n")
tea = Recipe("Tea")
tea.add_ingredients("Water", "Tea Leaves", "Sugar")
tea.set_cooking_time(5)
tea.get_difficulty()
print(tea)

coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)
coffee.get_difficulty()
print(coffee)

cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Extract", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)
cake.get_difficulty()
print(cake)

bananasmoothie = Recipe("Banana Smoothie")
bananasmoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
bananasmoothie.set_cooking_time(5)
bananasmoothie.get_difficulty()
print(bananasmoothie)
print("--------------------")

recipes_list = [tea, coffee, cake, bananasmoothie]

#Print recipes with certain ingredients
print("\nRecipes that contain Water: \n")
recipe_search(recipes_list, "Water")
print("--------------------")

print("\nRecipes that contain Sugar: \n")
recipe_search(recipes_list, "Sugar")
print("--------------------")

print("\nRecipes that contain Bananas: \n")
recipe_search(recipes_list, "Bananas")
print("--------------------")